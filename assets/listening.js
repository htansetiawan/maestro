// Keep comparison tracks from playing over one another.
const listeningPlayers = [...document.querySelectorAll('audio')];
listeningPlayers.forEach((player) => {
  if (!player.hasAttribute('aria-label')) {
    const heading = player.previousElementSibling;
    const title = heading?.matches('h2') ? heading.textContent : document.querySelector('h1').textContent;
    player.setAttribute('aria-label', title.trim());
  }
  player.addEventListener('play', () => {
    listeningPlayers.forEach((other) => {
      if (other !== player) other.pause();
    });
  });
});
