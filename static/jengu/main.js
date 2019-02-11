/**
 * @namespace jengu_main
 * @version 0.7.3
 * @author David, Zarebski [zarebskidavid@gmail.com]
 * @copyright David, Zarebski 2018-2019
 * @license GPLv3
 */
  function storeKey(){
     var inputName = document.getElementById("id_password");
     window.sessionStorage.id_password = md5(inputName.value);
    }

  function encrypt(t){
    var key = aesjs.utils.hex.toBytes(sessionStorage.getItem("id_password"));
    var textBytes = aesjs.utils.utf8.toBytes(t);
    var aesCtr = new aesjs.ModeOfOperation.ctr(key);
    var encryptedBytes = aesCtr.encrypt(textBytes);
    var encryptedHex = aesjs.utils.hex.fromBytes(encryptedBytes);
    return encryptedHex;
    }

  function decrypt(t){
    var key = aesjs.utils.hex.toBytes(sessionStorage.getItem("id_password"));
    var textBytes = aesjs.utils.hex.toBytes(t);
    var aesCtr = new aesjs.ModeOfOperation.ctr(key);
    var decriptedBytes = aesCtr.decrypt(textBytes);
    var decrypted_utf8 = aesjs.utils.utf8.fromBytes(decriptedBytes);
    return decrypted_utf8;
    }

  function encrypt_form(t){
    var key = aesjs.utils.hex.toBytes(sessionStorage.getItem("id_password"));
    var ids = t , len = ids.length;

    for (i = 0; i<len; i++){  
      text = document.getElementById(ids[i]).value
      var textBytes = aesjs.utils.utf8.toBytes(text);
      var aesCtr = new aesjs.ModeOfOperation.ctr(key);
      var encryptedBytes = aesCtr.encrypt(textBytes);
      var encryptedHex = aesjs.utils.hex.fromBytes(encryptedBytes);
      console.log(encryptedHex);
      document.getElementById(t[i]).value = encryptedHex;
    }
  }

  function decrypt_form(form){
    len = document.getElementById(form).options.length
  
    for (i = 1; i<len; i++){
      var fields = document.getElementById(form).options[i].text;
      fields = fields.split(', ');
      var date = fields[2];

      fields = fields.slice(0,2).map(t => decrypt(t));
      fields.push(date);
      fields = fields.join(", ");

      document.getElementById(form).options[i].text = fields;
  } 
}

  
  function download_csv(csv, filename) {
    var csvFile;
    var downloadLink;
    // CSV FILE
    csvFile = new Blob([csv], {type: "text/csv"});
    // Download link
    downloadLink = document.createElement("a");
    // File name
    downloadLink.download = filename;
    // We have to create a link to the file
    downloadLink.href = window.URL.createObjectURL(csvFile);
    // Make sure that the link is not displayed
    downloadLink.style.display = "none";
    // Add the link to your DOM
    document.body.appendChild(downloadLink);
    // Lanzamos
    downloadLink.click();
}

  function export_table_to_csv(html, filename) {
    var csv = [];
    var rows = document.querySelectorAll("table tr");
  
      for (var i = 0; i < rows.length; i++) {
        var row = [], cols = rows[i].querySelectorAll("td, th");
    
        for (var j = 0; j < cols.length; j++) 
            row.push(cols[j].innerText);
        
    csv.push(row.join(","));    
  }
    // Download CSV
    download_csv(csv.join("\n"), filename);
}


