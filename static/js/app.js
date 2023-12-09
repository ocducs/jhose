var timestamp = new Date().getTime();     
     
var el = document.getElementById("grafica");     
     
el.src = "/static/img/grafica.png?t=" + timestamp; 

function refreshImage(imgElement, imgURL){    
    // create a new timestamp 
    var timestamp = new Date().getTime();  
  
    var el = document.getElementById(imgElement);  
  
    var queryString = "?t=" + timestamp;    
   
    el.src = imgURL + queryString;    
}