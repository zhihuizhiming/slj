
var $wg = function(id){return document.getElementById(id)};
var viewall = 1,nowpage = 1;
var likeid = 0,liketype = 1,likearr = ['l','t','h'];
var picmore = 1,showmore = 1,gmp = 4;
//搜索检查
function searchnow(){
   if($wg('key').value == '搜妹子'){$wg('key').value = '';}
}
//执行搜索
function searchpic(){
   if($wg('key').value == ''){
      alert('请输入关键字再搜索');
      formsearch.key.focus();
      return false;
   }else if($wg('key').value == '搜妹子'){
      formsearch.key.focus();
      return false;
   }else{
      document.formsearch.submit();
   }
}
//点赞
function likemm(aid){
   if(likeid == aid){return false;}
   var d_n = new Date().getTime();
   likeid = aid;
   if(window.XMLHttpRequest){
      xmlhttp = new XMLHttpRequest;
      if(xmlhttp.overrideMimeType){
      xmlhttp.overrideMimeType('text/xml');
      }
   }else if(window.ActiveXObject){
      xmlhttp = new ActiveXObject('Microsoft.XMLHTTP');
   }
   xmlhttp.onreadystatechange = callback;
   xmlhttp.open('GET','http://www.92mn.bid/like.php?id='+aid,true);
   xmlhttp.send(null);
}
function callback(){
   if(xmlhttp.readyState==4 && xmlhttp.status==200){
      var renum = xmlhttp.responseText;
	  renum = parseInt(renum);
	  if(renum > 0){
         if(liketype == 1){
            $wg('like').innerText = '喜欢('+renum+')';
		 }else{
            $wg(likearr[liketype-2]+likeid).innerText = renum;
         }
	  }
   }
}
//显示更多图片
function morepic(mid){
   var gotourl = 'http://www.92mn.bid/getmore.php?page=';
   var ru_n = new Date().getTime();
   picmore = mid;
   if(showmore == 2 && picmore == 1){return false;}
   if(picmore == 2){
      gotourl += '9999';
   }else{
      gotourl += gmp;
   }
   if(window.XMLHttpRequest){
      xmlhttp = new XMLHttpRequest;
      if(xmlhttp.overrideMimeType){
         xmlhttp.overrideMimeType('text/xml');
      }
   }else if(window.ActiveXObject){
      xmlhttp = new ActiveXObject('Microsoft.XMLHTTP');
   }
   xmlhttp.onreadystatechange = moreback;
   xmlhttp.open('GET',gotourl+'&ra='+ru_n,true);
   xmlhttp.send(null);
}
function moreback(){
   if(xmlhttp.readyState==4 && xmlhttp.status==200){
      var repic = xmlhttp.responseText;
	  if(picmore == 1){
	     if(repic == ''){
		    showmore = 2;
		    $wg('showmore').innerText = '没有了不用点了';
	     }else{
		    $wg('article').insertAdjacentHTML('beforeEnd',repic);
		    gmp++;
	     }
	  }else{
         repic = '<dt>美图推荐</dt>' + repic;
		 $wg('hot').innerHTML = repic;
      }
   }
}

//浏览图片
function openall(pid){
   var showall = '';
   var imgurl = '<img src="http://m.92mn.bid/ip/';
   if(viewall == 1){
      if(pid != picinfo[2]){
         for(var p=pid;p<picinfo[2];p++){showall = showall+imgurl+imglist[p]+'" />';}
		 if(pid > 1){
			for(var u=1;u<pid;u++){showall = showall+imgurl+imglist[u]+'" />';}
		 }
		 nowpage = pid;
		 viewall = 2;
		 $wg('viewall').className = 'viewall on';
		 $wg('opic').className = 'ch all on';
		 $wg('opic').innerText = '收起图片';
		 $wg('content').innerHTML = showall;
      }
   }else{
      viewall = 1;
	  $wg('viewall').className = 'viewall';
	  $wg('opic').className = 'ch all';
	  $wg('opic').innerText = '全部图片';
	  showall = imgurl+imglist[nowpage]+'" />';
	  $wg('content').innerHTML = showall;
   }
}