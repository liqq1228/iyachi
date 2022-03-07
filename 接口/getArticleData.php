<?php
require_once('./SqlHelper.class.php');
class BaseObject{

}
$mySqlHelper=new SqlHelper();
//$article_index=$_GET['question_number'];
//$sql="select * from QGNews where article_index=".$article_index;
$sql="select * from SZXX";
//echo $sql;
$mydata=$mySqlHelper->execute_dql2($sql);//数组
print($mydata)
//echo count($mydata);
echo json_encode($mydata,JSON_UNESCAPED_UNICODE);
?>