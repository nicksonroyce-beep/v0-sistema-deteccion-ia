// Mostrar y ocultar mensajes flash automáticamente
document.addEventListener("DOMContentLoaded", () => {
  const flashes = document.querySelectorAll(".flash")
  flashes.forEach((flash) => {
    setTimeout(() => {
      flash.style.display = "none"
    }, 4000) // se ocultan después de 4 segundos
  })

  class ParticleSystem {
    constructor() {
      this.canvas = document.createElement("canvas")
      this.ctx = this.canvas.getContext("2d")
      this.particles = []
      this.mouse = { x: 0, y: 0 }
      this.init()
    }

    init() {
      this.canvas.id = "particle-canvas"
      this.canvas.style.position = "fixed"
      this.canvas.style.top = "0"
      this.canvas.style.left = "0"
      this.canvas.style.width = "100%"
      this.canvas.style.height = "100%"
      this.canvas.style.zIndex = "-1"
      this.canvas.style.pointerEvents = "none"
      document.body.appendChild(this.canvas)

      this.resize()
      this.createParticles()
      this.bindEvents()
      this.animate()
    }

    resize() {
      this.canvas.width = window.innerWidth
      this.canvas.height = window.innerHeight
    }

    createParticles() {
      const particleCount = Math.floor((this.canvas.width * this.canvas.height) / 15000)
      for (let i = 0; i < particleCount; i++) {
        this.particles.push({
          x: Math.random() * this.canvas.width,
          y: Math.random() * this.canvas.height,
          vx: (Math.random() - 0.5) * 0.5,
          vy: (Math.random() - 0.5) * 0.5,
          size: Math.random() * 2 + 1,
          opacity: Math.random() * 0.5 + 0.2,
          hue: Math.random() * 60 + 200, // Azul a púrpura
        })
      }
    }

    bindEvents() {
      window.addEventListener("resize", () => this.resize())
      document.addEventListener("mousemove", (e) => {
        this.mouse.x = e.clientX
        this.mouse.y = e.clientY
      })
    }

    animate() {
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height)

      this.particles.forEach((particle, index) => {
        // Movimiento base
        particle.x += particle.vx
        particle.y += particle.vy

        // Atracción al mouse
        const dx = this.mouse.x - particle.x
        const dy = this.mouse.y - particle.y
        const distance = Math.sqrt(dx * dx + dy * dy)

        if (distance < 150) {
          const force = (150 - distance) / 150
          particle.vx += dx * force * 0.0001
          particle.vy += dy * force * 0.0001
        }

        // Límites del canvas
        if (particle.x < 0 || particle.x > this.canvas.width) particle.vx *= -1
        if (particle.y < 0 || particle.y > this.canvas.height) particle.vy *= -1

        // Dibujar partícula
        this.ctx.beginPath()
        this.ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2)
        this.ctx.fillStyle = `hsla(${particle.hue}, 70%, 60%, ${particle.opacity})`
        this.ctx.fill()

        // Conectar partículas cercanas
        for (let j = index + 1; j < this.particles.length; j++) {
          const other = this.particles[j]
          const dx2 = particle.x - other.x
          const dy2 = particle.y - other.y
          const distance2 = Math.sqrt(dx2 * dx2 + dy2 * dy2)

          if (distance2 < 100) {
            this.ctx.beginPath()
            this.ctx.moveTo(particle.x, particle.y)
            this.ctx.lineTo(other.x, other.y)
            this.ctx.strokeStyle = `hsla(${particle.hue}, 70%, 60%, ${(0.1 * (100 - distance2)) / 100})`
            this.ctx.lineWidth = 0.5
            this.ctx.stroke()
          }
        }
      })

      requestAnimationFrame(() => this.animate())
    }
  }

  new ParticleSystem()
})
