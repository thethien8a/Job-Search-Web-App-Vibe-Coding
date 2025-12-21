import { Loader2 } from 'lucide-react'

function LoadingSpinner({ size = 'md', text = 'Đang tải...' }) {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
  }

  return (
    <div className="flex flex-col items-center justify-center py-12">
      <Loader2 className={`${sizeClasses[size]} text-primary-600 animate-spin`} />
      {text && <p className="mt-4 text-gray-500">{text}</p>}
    </div>
  )
}

export default LoadingSpinner
