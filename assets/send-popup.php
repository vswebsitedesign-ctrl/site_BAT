<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $name     = htmlspecialchars(strip_tags(trim($_POST['name'] ?? '')));
    $phone    = htmlspecialchars(strip_tags(trim($_POST['phone'] ?? '')));
    $postcode = htmlspecialchars(strip_tags(trim($_POST['postcode'] ?? '')));
    if (empty($name) || empty($phone) || empty($postcode)) {
        http_response_code(400);
        exit('Missing required fields.');
    }
    $to      = 'darren@buildingsandtrust.co.uk';
    $subject = 'New quick-quote enquiry from ' . $name;
    $body    = "Name: $name\nPhone: $phone\nPostcode: $postcode";
    $headers = "From: noreply@buildingsandtrust.co.uk\r\n";
    if (mail($to, $subject, $body, $headers)) {
        header('Location: /thank-you/');
        exit;
    } else {
        http_response_code(500);
        exit('Mail failed. Please try again.');
    }
} else {
    http_response_code(405);
    exit('Method not allowed.');
}
?>
