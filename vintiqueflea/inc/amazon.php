<?php
defined('INC') || exit;
/**
 * Amazon Product Advertising API 5.0 integration.
 *
 * Product images and product links on the shop cards come from the PA-API, which is the
 * Associates-approved way to show Amazon product images (Amazon hosts the images; we only
 * cache the image URL, never the file). Keys live ONLY on the server in data/amazon.php:
 *   <?php return ['access' => 'AKIA…', 'secret' => '…'];
 * tools/refresh-amazon.php refreshes data/amazon-cache.php daily (cron). Entries older than
 * 48h are ignored, so cards fall back to the photo style rather than show stale data.
 */

const AMAZON_CACHE_MAX_AGE = 172800;

function amazon_key(array $p): string
{
    return !empty($p['asin']) ? 'asin:' . $p['asin'] : 'q:' . strtolower(trim($p['q'] ?? $p['name']));
}

function amazon_cache(): array
{
    static $c = null;
    if ($c === null) {
        $f = DATA_DIR . '/amazon-cache.php';
        $c = is_file($f) ? (array) (include $f) : [];
    }
    return $c;
}

/** Fresh PA-API data for a product, or null. */
function amazon_item(array $p): ?array
{
    $hit = amazon_cache()[amazon_key($p)] ?? null;
    return ($hit && !empty($hit['img']) && (time() - ($hit['t'] ?? 0)) < AMAZON_CACHE_MAX_AGE) ? $hit : null;
}

function paapi_credentials(): ?array
{
    $f = DATA_DIR . '/amazon.php';
    $c = is_file($f) ? include $f : null;
    return is_array($c) && !empty($c['access']) && !empty($c['secret']) ? $c : null;
}

/** Signed PA-API 5 call (AWS SigV4). Returns decoded JSON or ['__error' => …]. */
function paapi_call(string $operation, array $payload, array $creds): array
{
    $host = 'webservices.amazon.com';
    $region = 'us-east-1';
    $service = 'ProductAdvertisingAPI';
    $path = '/paapi5/' . strtolower($operation);
    $payload += ['PartnerTag' => AMAZON_TAG, 'PartnerType' => 'Associates', 'Marketplace' => 'www.amazon.com'];
    $body = json_encode($payload, JSON_UNESCAPED_SLASHES);
    $amzDate = gmdate('Ymd\THis\Z');
    $date = substr($amzDate, 0, 8);
    $headers = [
        'content-encoding' => 'amz-1.0',
        'content-type' => 'application/json; charset=utf-8',
        'host' => $host,
        'x-amz-date' => $amzDate,
        'x-amz-target' => 'com.amazon.paapi5.v1.ProductAdvertisingAPIv1.' . $operation,
    ];
    $canonHeaders = '';
    foreach ($headers as $k => $v) {
        $canonHeaders .= $k . ':' . $v . "\n";
    }
    $signedHeaders = implode(';', array_keys($headers));
    $canonical = "POST\n$path\n\n$canonHeaders\n$signedHeaders\n" . hash('sha256', $body);
    $scope = "$date/$region/$service/aws4_request";
    $toSign = "AWS4-HMAC-SHA256\n$amzDate\n$scope\n" . hash('sha256', $canonical);
    $k = hash_hmac('sha256', $date, 'AWS4' . $creds['secret'], true);
    $k = hash_hmac('sha256', $region, $k, true);
    $k = hash_hmac('sha256', $service, $k, true);
    $k = hash_hmac('sha256', 'aws4_request', $k, true);
    $auth = "AWS4-HMAC-SHA256 Credential={$creds['access']}/$scope, SignedHeaders=$signedHeaders, Signature=" . hash_hmac('sha256', $toSign, $k);

    $send = [];
    foreach ($headers as $k2 => $v) {
        $send[] = "$k2: $v";
    }
    $send[] = "Authorization: $auth";
    $ch = curl_init("https://$host$path");
    curl_setopt_array($ch, [CURLOPT_POST => true, CURLOPT_POSTFIELDS => $body, CURLOPT_HTTPHEADER => $send, CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 20]);
    $res = curl_exec($ch);
    $code = (int) curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $err = curl_error($ch);
    curl_close($ch);
    $json = is_string($res) ? json_decode($res, true) : null;
    if ($code !== 200 || !is_array($json)) {
        $msg = $json['Errors'][0]['Code'] ?? ($err ?: "HTTP $code");
        return ['__error' => $msg . (isset($json['Errors'][0]['Message']) ? ': ' . $json['Errors'][0]['Message'] : '')];
    }
    return $json;
}

/** Every product the site displays (shop, guides, food trucks). */
function all_products(): array
{
    $list = [];
    foreach (SHOP as $c) {
        foreach ($c['products'] as $p) {
            $list[amazon_key($p)] = $p;
        }
    }
    foreach (load_guides() as $g) {
        foreach ($g['products'] ?? [] as $p) {
            $list[amazon_key($p)] = $p;
        }
    }
    foreach (FOOD_TRUCK_PICKS as $p) {
        $list[amazon_key($p)] = $p;
    }
    return $list;
}
