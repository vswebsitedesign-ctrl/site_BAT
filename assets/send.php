<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $name     = htmlspecialchars(strip_tags(trim($_POST['name'] ?? '')));
    $email    = htmlspecialchars(strip_tags(trim($_POST['email'] ?? '')));
    $phone    = htmlspecialchars(strip_tags(trim($_POST['phone'] ?? '')));
    $postcode = htmlspecialchars(strip_tags(trim($_POST['postcode'] ?? '')));
    $service  = htmlspecialchars(strip_tags(trim($_POST['service'] ?? '')));
    $message  = htmlspecialchars(strip_tags(trim($_POST['message'] ?? '')));

    if (empty($name) || empty($phone) || empty($postcode)) {
        http_response_code(400);
        exit('Missing required fields.');
    }

    if (!empty($email) && !filter_var($email, FILTER_VALIDATE_EMAIL)) {
        http_response_code(400);
        exit('Invalid email address.');
    }

    $to      = 'darren@buildingsandtrust.co.uk';
    $subject = 'New enquiry from ' . $name;
    $body    = "Name: $name\nPhone: $phone\nPostcode: $postcode\nEmail: $email\nService: $service\n\nMessage:\n$message";
    $headers = "From: noreply@buildingsandtrust.co.uk\r\n" . (!empty($email) ? "Reply-To: $email\r\n" : '');

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
