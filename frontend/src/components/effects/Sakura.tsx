import { useEffect, useRef } from 'react'

interface SakuraProps {
  count?: number
  speed?: number
  color?: string
}

export function SakuraEffect({ count = 30, speed = 2, color = '#ffb7c5' }: SakuraProps) {
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!containerRef.current) return

    const container = containerRef.current
    const petals: HTMLDivElement[] = []

    for (let i = 0; i < count; i++) {
      const petal = document.createElement('div')
      petal.className = 'absolute rounded-full opacity-60'
      const size = Math.random() * 8 + 4
      petal.style.width = `${size}px`
      petal.style.height = `${size}px`
      petal.style.backgroundColor = color
      petal.style.left = `${Math.random() * 100}%`
      petal.style.top = `-20px`
      petal.style.animation = `fall ${Math.random() * 3 + 4}s linear infinite`
      petal.style.animationDelay = `${Math.random() * 5}s`
      container.appendChild(petal)
      petals.push(petal)
    }

    return () => {
      petals.forEach(petal => petal.remove())
    }
  }, [count, speed, color])

  return (
    <div ref={containerRef} className="sakura-container overflow-hidden w-full h-full relative">
      <style>{`
        @keyframes fall {
          0% {
            transform: translateY(0) rotate(0deg) translateX(0);
            opacity: 0.6;
          }
          50% {
            opacity: 0.8;
          }
          100% {
            transform: translateY(100vh) rotate(720deg) translateX(100px);
            opacity: 0;
          }
        }
      `}</style>
    </div>
  )
}
