document.getElementById('table').addEventListener('click', function() {
var list = document.getElementById('list');
  if (list.style.display === 'none') {
    list.style.display = 'block';
  } else {
    list.style.display = 'none';
  }
});
