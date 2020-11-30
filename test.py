  from browser import document
  from browser.widgets.dialog import InfoDialog


  def alert(event):
    InfoDialog("Hello", "버튼이 눌렸다!")
    
  document["test-button"].bind("click", alert)