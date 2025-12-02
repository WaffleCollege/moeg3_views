const picker = document.querySelector('#picker');   // DOMをひろう

const setBgColor = () => {
  document.body.style.backgroundColor = picker.value;   // メソッドを定義
 }

picker.addEventListener('input', setBgColor)    // イベントが起こったらsetBgColorを実行（イベントが起こるまで待つ）