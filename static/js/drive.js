// for progress tag in HTML 
function tag () {
    let progress = document.querySelector('.progressTag')
    let interval = 1
    let updatesPerSecond = 1000 / 60
    // 드라이브 용량 가지고 와서 여기서 바꾸면 됨ㄴ
    let end = progress.max * 0.12
  
    function animator () {
      progress.value = progress.value + interval
      if ( progress.value + interval < end){
        setTimeout(animator, updatesPerSecond);
      } else { 
        progress.value = end
      }
    }
  
    setTimeout(() => {
      animator()
    }, updatesPerSecond)
  }
  
  tag()