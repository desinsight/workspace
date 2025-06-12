import React, { useEffect, useState } from 'react'
import { Badge } from '@/components/common/Badge'
import { Button } from '@/components/common/Button'
import { RefreshCw } from 'lucide-react'
import { ollamaService } from '@/services/ollama'

export const ServerStatus: React.FC = () => {
  const [isConnected, setIsConnected] = useState<boolean | null>(null)
  const [isChecking, setIsChecking] = useState(false)

  const checkConnection = async () => {
    setIsChecking(true)
    try {
      await ollamaService.listModels()
      setIsConnected(true)
    } catch (error) {
      console.error('Failed to connect to Ollama server:', error)
      setIsConnected(false)
    } finally {
      setIsChecking(false)
    }
  }

  useEffect(() => {
    checkConnection()
  }, [])

  if (isConnected === null) {
    return (
      <div className="flex items-center space-x-2">
        <Badge variant="default">Checking...</Badge>
      </div>
    )
  }

  return (
    <div className="flex items-center space-x-2">
      <Badge
        variant={isConnected ? 'success' : 'error'}
      >
        {isConnected ? 'Connected' : 'Disconnected'}
      </Badge>
      <Button
        variant="ghost"
        size="sm"
        onClick={checkConnection}
        disabled={isChecking}
      >
        <RefreshCw className={`h-4 w-4 ${isChecking ? 'animate-spin' : ''}`} />
      </Button>
    </div>
  )
} 