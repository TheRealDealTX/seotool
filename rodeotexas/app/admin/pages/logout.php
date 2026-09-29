<?php
declare(strict_types=1);

if (is_post()) {
    RT\Auth::logout();
}
redirect(admin_url('login'), 303);
