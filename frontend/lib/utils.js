export function formatPercent(x) {
    return `${(x * 100).toFixed(1)}%`
  }
  
  export function truncate(text, n = 120) {
    if (!text) return ''
    return text.length > n ? `${text.slice(0, n)}…` : text
  }
  