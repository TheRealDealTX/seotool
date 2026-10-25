"""Package out/public_html for deployment: adds a manifest-based cleanup script.
usage: python3 make_deploy.py OUT_DIR ZIP_PATH  (prints the one-time cleanup token)"""
import os, sys, secrets, zipfile, json
out, zpath = os.path.abspath(sys.argv[1]), sys.argv[2]
web = os.path.join(out, 'public_html')
token = secrets.token_hex(16)
files = []
for root, _, fs in os.walk(web):
    for f in fs:
        files.append(os.path.relpath(os.path.join(root, f), web).replace(os.sep, '/'))
script = """<?php
// One-time post-deploy cleanup: removes files that are not part of this build.
if (!hash_equals('%s', (string) ($_GET['token'] ?? ''))) { http_response_code(404); exit; }
header('Content-Type: text/plain');
$keep = array_flip(json_decode('%s', true));
$keep['ce-deploy-%s.php'] = true;
$preserve = '#^ce-private/(mail-config\\.php|[^/]+\\.log\\.php)$#';
$root = __DIR__;
$removed = 0;
$it = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($root, FilesystemIterator::SKIP_DOTS), RecursiveIteratorIterator::CHILD_FIRST);
foreach ($it as $f) {
    $rel = str_replace('\\\\', '/', substr($f->getPathname(), strlen($root) + 1));
    if ($f->isDir()) { @rmdir($f->getPathname()); continue; }
    if (isset($keep[$rel]) || preg_match($preserve, $rel)) { continue; }
    if (@unlink($f->getPathname())) { $removed++; echo "removed $rel\\n"; }
}
echo "done, removed $removed files\\n";
@unlink(__FILE__);
""" % (token, json.dumps(files).replace("'", "\\'"), token)
name = 'ce-deploy-%s.php' % token
with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as z:
    for rel in files:
        z.write(os.path.join(web, rel), rel)
    z.writestr(name, script)
print(name)
