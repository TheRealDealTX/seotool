<?php
// The old store's login page. The new site has no accounts; send visitors to their cart.
header('Location: /cart/', true, 301);
