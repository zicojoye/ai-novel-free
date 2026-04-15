import { useEffect, useRef } from 'react'

interface BubbleProps {
  count?: number
  speed?: number
  color?: string
}

export function BubbleEffect({ count = 20, speed = 1.5, color = '#87ceeb' }: BubbleProps) {
  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!containerRef.current) return

    // 创建简单的气泡效果
    const container = containerRef.current
    const bubbles: HTMLDivElement[] = []

    for (let i = 0; i < count; i++) {
      const bubble = document.createElement('div')
      bubble.className = 'absolute rounded-full opacity-60'
      bubble.style.width = `${Math.random() * 20 + 10}px`
      bubble.style.height = bubble.style.width
      bubble.style.backgroundColor = color
      bubble.style.left = `${Math.random() * 100}%`
      bubble.style.top = `${Math.random() * 100}%`
      bubble.style.animation = `float ${Math.random() * 3 + 2}s ease-in-out infinite`
      bubble.style.animationDelay = `${Math.random() * 2}s`
      container.appendChild(bubble)
      bubbles.push(bubble)
    }

    return () => {
      bubbles.forEach(bubble => bubble.remove())
    }
  }, [count, speed, color])

  return (
    <div ref={containerRef} className="bubble-container overflow-hidden w-full h-full relative">
      <style>{`
        @keyframes float {
          0%, 100% { transform: translateY(0) translateX(0); }
          50% { transform: translateY(-20px) translateX(10px); }
        }
      `}</style>
    </div>
  )
}
