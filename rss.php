<?php 
set_time_limit(0);
flush();
ob_flush();
$count = 0;
date_default_timezone_set("Asia/Calcutta");
//while(true)
//{
	$data = array();
	$k = 0;

	for($i=0;$i<=14;$i++)
	{
		switch($i)
		{
			case 0:
					$url = 'http://economictimes.indiatimes.com/Markets/markets/rssfeeds/1977021501.cms'; 
					$newspaper = 'Economic Times';
					break;
			case 1:
					$url = 'http://economictimes.indiatimes.com/news/international/business/articlelist/26519199.cms';
					$newspaper = 'Economic Times';
					break;
			case 8:
					$url = 'http://feeds.reuters.com/reuters/globalmarketsNews?format=xml';
					$newspaper = 'Reuters';
					break;
			case 2: 
					$url = 'http://feeds.reuters.com/reuters/businessNews?format=xml';
					$newspaper = 'Reuters';
					break;
			case 3: 
					$url = 'http://www.economist.com/sections/business-finance/rss.xml';
					$newspaper = 'The Economist';
					break;
			case 4: 
					$url = 'http://www.business-standard.com/rss/markets-106.rss';
					$newspaper = 'Business Standard';
					break;
			case 5:
					$url = 'http://www.business-standard.com/rss/finance-103.rss';
					$newspaper = 'Business Standard';
					break;
			case 6:
					$url = 'http://feeds.bbci.co.uk/news/business/rss.xml';
					$newspaper = 'BBC';	
					break;
			case 7 :
					$url = 'http://timesofindia.feedsportal.com/c/33039/f/533919/index.rss';
					$newspaper = 'BBC';	
					break;				
			
			case 9:
					$url = 'http://www.forbes.com/markets/index.xml';
					$newspaper = 'Forbes';	
					break;
					
			case 10:
					$url = 'http://www.forbes.com/business/index.xml';
					$newspaper = 'Forbes';	
					break;
					
			case 11:
					$url = 'http://www.forbes.com/finance/index.xml';
					$newspaper = 'Forbes';
					break;
					
			case 12:
					$url = 'http://www.cnbc.com/id/100727362/device/rss/rss.html';
					$newspaper = 'CNBC';
					break;
					
			case 13:
					$url = 'http://www.cnbc.com/id/10001147/device/rss/rss.html';
					$newspaper = 'CNBC';
					break;
					
			case 14: 
					$url = 'http://www.cnbc.com/id/20910258/device/rss/rss.html';
					$newspaper = 'CNBC';
					break;
					
			case 15: 
					$url = 'http://www.ft.com/rss/world';
					$newspaper = 'Finance Times';
					break;
					
			case 16: 
					$url = 'http://www.ft.com/rss/companies/financials';
					$newspaper = 'Finance Times';
					break;
		}			
		$rss = simplexml_load_file($url, null, LIBXML_NOCDATA);
		foreach($rss->channel->item as $item) {
			$count ++;
			$title = (string) $item->title;
			$link = (string) $item->link;
			$description = (string) $item->description;
			$fields = array('url'=>$link);
			$res = file_get_contents('http://localhost/fivefilters-full-text-rss/extract.php?url='.$link);
			$json=utf8_decode($res);
			$obj = json_decode($json);
			$date = (string) $item->pubDate;
			$pubdate = date('r',strtotime($date));
			$processedData = preg_replace("/<.*?>/","",$obj->content);
			array_push($data, array("title" => $title, "content" => $processedData, "pubdate"=> $pubdate, "newspaper" => $newspaper));
			echo " Title: $title " ;?><br/> 
			<?php
			echo "Website : $newspaper " ;
			?>
			<br/>
			<?php
			echo "PubDate : $pubdate " ;
			?>
			<br/> 
			<?php 
			flush();
			ob_flush();
		}	
		$i++;
	}
	$array["root"] = $data;
	$file_count_p = fopen('file_count.txt', 'r+');
	$c = fread($file_count_p,filesize('file_count.txt'));
	fseek($file_count_p,0,SEEK_SET);
	$c++;
	fwrite($file_count_p, $c);
	$fpw = fopen('DataCorpus_Anu/results'.$c.'.json', 'w');
	fwrite($fpw,json_encode($array));
	fclose($fpw);
	//sleep(1800);
//}	
?>