<?php
$db = new mysqli("sql101.infinityfree.com", "if0_36955835", "80IcbahAQJqeal", "if0_36955835_messages"); //server,user,pass,db


$OK = 200; // Successful
$ACCEPTED = 202; // Accepted for processing
$BAD_REQUEST = 400; // Bad request
$UNAUTHORIZED = 401; // Unauthorized
$FORBIDDEN = 403; // Forbidden
http_response_code($BAD_REQUEST);

function isset_in($holding, $list)
{
    foreach ($list as $item) {
        if (!isset($holding[$item])) {
            return false;
        }
    }
    return true;
}

$post_data = file_get_contents("php://input");
$data = json_decode($post_data, true);
if (isset_in($data, array("user", "command"))) {
    $user = $data['user'];
    $reponse = [];
    $reponse["allow"] = false;
    switch ($data["command"]) {
        case 'login':
            if (!(isset_in($data, array("pasw")))) {
                break;
            }
            $pasw = $data['pasw'];
            $sql = "SELECT * FROM `users` WHERE username = '$user' and password = '$pasw'";
            $res = mysqli_query($db, $sql);
            $rows = mysqli_num_rows($res);
            if ($res and $rows != 0) {
                $reponse["allow"] = true;
            }
            http_response_code($OK);
            break;
        case 'signup':
            if (!(isset_in($data, array("pasw")))) {
                break;
            }
            $pasw = $data['pasw'];
            $sql = "SELECT * FROM `users` WHERE username = '$user'";
            $res = mysqli_query($db, $sql);
            $rows = mysqli_num_rows($res);
            if ($res and $rows > 0) {
                break;
            }
            $sql = "INSERT INTO users (username,password) VALUES ('$user','$pasw')";
            $res = mysqli_query($db, $sql);
            if (!($res)) {
                break;
            }
            $reponse["allow"] = True;
            http_response_code($OK);
            break;
        case 'message':
            if (!(isset_in($data, array("to", "message")))) {
                break;
            }
            $to = $data['to'];
            $message = $data['message'];
            $sql = "INSERT INTO messages (sender,reciever,message) VALUES ('$user','$to','$message')";
            $res = mysqli_query($db, $sql);
            if (!($res)) {
                break;
            }
            $reponse["allow"] = True;
            http_response_code($OK);
            break;
        case 'get_message':
            $sql = "SELECT * FROM `messages` WHERE sender = '$user' or reciever = '$user' ORDER BY timestamp DESC";
            $res = mysqli_query($db, $sql);
            $rows = mysqli_num_rows($res);
            $reponse["messages"] = [];
            if ($res and $rows >= 0) {
                while ($tdata = mysqli_fetch_assoc($res)) {
                    array_push($reponse["messages"], $tdata);
                }
            }
            $reponse["allow"] = true;
            http_response_code($OK);
            break;
    }
    echo json_encode($reponse);
}
