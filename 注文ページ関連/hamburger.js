function DisplayDate() {
			// 選択されている<option>要素を取り出す
      var selected = $("#neta1").children("option:selected"); //「option」は省略可
				
      // 値を取り出す
      var selectedValue = selected.val();

  alert(selectedValue);
}
document.querySelector('.hamburger').addEventListener('click', function(){
    this.classList.toggle('active');
    document.querySelector('.slide-menu').classList.toggle('active');
  })