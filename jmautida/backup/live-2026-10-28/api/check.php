<?php
declare(strict_types=1);
require_once __DIR__ . '/lib.php';
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('X-Content-Type-Options: nosniff');
try {
    if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
        header('Allow: POST');
        throw new CheckError('Use POST to submit a website check.', 405);
    }
    if (strtolower(explode(';', $_SERVER['CONTENT_TYPE'] ?? '')[0]) !== 'application/json') {
        throw new CheckError('Send a JSON request.', 415);
    }
    $raw = file_get_contents('php://input', false, null, 0, 4097);
    if ($raw === false || strlen($raw) > 4096) throw new CheckError('Request is too large.', 413);
    $input = json_decode($raw, true);
    if (!is_array($input) || !is_string($input['url'] ?? null) || !in_array($input['mode'] ?? '', ['meta', 'favicon'], true)) {
        throw new CheckError('Provide a website URL and a valid check mode.', 400);
    }
    if (!extension_loaded('curl') || !class_exists('DOMDocument')) throw new CheckError('Enable PHP cURL and DOM/XML in your hosting PHP settings.', 503);
    validate_url($input['url']);
    rate_limit();
    $fetcher = new PublicFetcher();
    $page = $fetcher->get($input['url']);
    if ($page['status'] < 200 || $page['status'] >= 300) throw new CheckError('The website returned HTTP ' . $page['status'] . '. It may block automated checks.', 422);
    if (!preg_match('~(?:text/html|application/xhtml\+xml)~i', $page['type'])) throw new CheckError('The URL did not return an HTML page.', 422);
    $doc = html_document($page['body']);
    $result = $input['mode'] === 'meta' ? inspect_meta($doc, $page['url']) : inspect_icons($doc, $page['url'], $fetcher);
    echo json_encode(['url' => $page['url'], 'status' => $page['status']] + $result, JSON_UNESCAPED_SLASHES | JSON_INVALID_UTF8_SUBSTITUTE);
} catch (CheckError $error) {
    http_response_code($error->getCode() >= 400 ? $error->getCode() : 422);
    echo json_encode(['error' => $error->getMessage()], JSON_INVALID_UTF8_SUBSTITUTE);
} catch (Throwable $error) {
    http_response_code(500);
    echo json_encode(['error' => 'The server could not complete the check. Please try again later.']);
}
