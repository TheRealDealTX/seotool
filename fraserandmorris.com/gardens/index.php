<?php
// /gardens/ is a real folder (it holds the old courtyard/courtyard2.jpg image), so the
// host answers it before index.php. Send it to the gardens overview page.
header('Location: https://fraserandmorris.com/gardens.html', true, 301);
