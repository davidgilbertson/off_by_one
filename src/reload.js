const POLL_INTERVAL = 1000

const fetchLastModified = () => fetch(document.location, {method: 'HEAD'})
    .then(res => res.headers.get('last-modified'))

fetchLastModified().then(lastModified => {
  setInterval(() => {
    if (document.hidden) return

    fetchLastModified().then(lastModified2 => {
      if (lastModified !== lastModified2) document.location.reload()
    })
  }, POLL_INTERVAL)
})
