<?php
/**
 * Capstone Tek: contact form handler.
 * Receives the form on index.html and emails it to the address below.
 * Upload this file next to index.html (in public_html).
 */

$TO_EMAIL   = 'support@capstonetek.com';   // where enquiries are delivered
$FROM_EMAIL = 'support@capstonetek.com';   // must be a mailbox on your own domain
$SITE_NAME  = 'Capstone Tek Website';

header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('Cache-Control: no-store');

function respond($ok, $error = '', $code = 200) {
    http_response_code($code);
    echo json_encode($ok ? ['ok' => true] : ['ok' => false, 'error' => $error]);
    exit;
}

function field($key, $max, $multiline = false) {
    $value = isset($_POST[$key]) ? (string) $_POST[$key] : '';
    $value = trim(str_replace("\0", '', $value));
    if (!$multiline) {
        $value = preg_replace('/[\r\n\t]+/', ' ', $value);   // no header injection through single-line fields
    }
    if (function_exists('mb_substr')) {
        return mb_substr($value, 0, $max, 'UTF-8');
    }
    return substr($value, 0, $max);
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    respond(false, 'method_not_allowed', 405);
}

// Spam checks: the hidden "website" field must stay empty, and a person takes a few seconds to fill the form.
if (field('website', 200) !== '') {
    respond(true);                              // pretend success so bots move on
}
$elapsed = (int) field('t', 20);             // milliseconds the visitor spent on the page before sending
if ($elapsed > 0 && $elapsed < 3000) {
    respond(false, 'too_fast', 400);
}

$name     = field('name', 100);
$company  = field('company', 120);
$email    = field('email', 160);
$phone    = field('phone', 40);
$category = field('category', 60);
$message  = field('message', 4000, true);

if (strlen($name) < 2 || strlen($message) < 3) {
    respond(false, 'missing_fields', 422);
}
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    respond(false, 'invalid_email', 422);
}

$subject = 'Website enquiry from ' . $name . ($company !== '' ? ' (' . $company . ')' : '');
$encodedSubject = function_exists('mb_encode_mimeheader')
    ? mb_encode_mimeheader($subject, 'UTF-8', 'B', "\r\n")
    : '=?UTF-8?B?' . base64_encode($subject) . '?=';

$body  = "New enquiry from capstonetek.com\n";
$body .= str_repeat('-', 40) . "\n";
$body .= "Name:             $name\n";
$body .= "Company / brand:  " . ($company !== '' ? $company : '-') . "\n";
$body .= "Email:            $email\n";
$body .= "Phone:            " . ($phone !== '' ? $phone : '-') . "\n";
$body .= "Product category: " . ($category !== '' ? $category : '-') . "\n";
$body .= str_repeat('-', 40) . "\n\n";
$body .= $message . "\n\n";
$body .= str_repeat('-', 40) . "\n";
$body .= 'Sent ' . gmdate('Y-m-d H:i') . " UTC from IP " . ($_SERVER['REMOTE_ADDR'] ?? 'unknown') . "\n";

$headers  = 'From: ' . $SITE_NAME . ' <' . $FROM_EMAIL . ">\r\n";
$headers .= 'Reply-To: ' . $email . "\r\n";
$headers .= "MIME-Version: 1.0\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
$headers .= "Content-Transfer-Encoding: 8bit\r\n";
$headers .= 'X-Mailer: PHP/' . phpversion();

$sent = @mail($TO_EMAIL, $encodedSubject, $body, $headers, '-f' . $FROM_EMAIL);
if (!$sent) {
    respond(false, 'mail_failed', 500);
}
respond(true);
