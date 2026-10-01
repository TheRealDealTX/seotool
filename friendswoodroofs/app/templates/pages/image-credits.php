<?php
$images = require FR_APP . '/content/images.php';
partial('page-hero', [
    'title'   => 'Image Credits',
    'lead'    => 'The photographs on this website are openly licensed images from Wikimedia Commons, used for illustration. They are not photos of Friendswood Roofers projects.',
    'actions' => false,
]);
?>
<section class="section section--first">
  <div class="container prose legal">
    <p>Images were cropped to a 3:2 frame and resized for the web. Where a license is Creative Commons Attribution-ShareAlike (CC BY-SA), the cropped and resized versions published here are shared under the same license as the original.</p>
    <div class="table-wrap">
      <table>
        <caption class="sr-only">Photo sources and licenses</caption>
        <thead><tr><th scope="col">Photo</th><th scope="col">Original title</th><th scope="col">Author</th><th scope="col">License</th></tr></thead>
        <tbody>
        <?php foreach ($images as $key => $img): ?>
          <tr>
            <td class="credit-thumb"><img src="/assets/img/<?= e($key) ?>-480.webp" width="120" height="80" alt="<?= e($img['alt']) ?>" loading="lazy" decoding="async"></td>
            <td><a href="<?= e($img['source']) ?>" rel="noopener"><?= e($img['title']) ?></a></td>
            <td><?= e($img['author']) ?></td>
            <td><?= $img['license_url'] ? '<a href="' . e($img['license_url']) . '" rel="noopener license">' . e($img['license']) . '</a>' : e($img['license']) ?></td>
          </tr>
        <?php endforeach; ?>
        </tbody>
      </table>
    </div>
    <p>Icons and the Friendswood Roofers logo were created for this website.</p>
  </div>
</section>
