import React, { useState } from 'react'
import { ChatInterface } from '@/components/ollama/ChatInterface'
import { ModelManager } from '@/components/ollama/ModelManager'
import { ServerStatus } from '@/components/ollama/ServerStatus'
import { Button } from '@/components/common/Button'
import { MessageSquare, Settings } from 'lucide-react'

export const OllamaPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'chat' | 'models'>('chat')

  return (
    <div className="flex h-full flex-col">
      <div className="border-b p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <Button
              variant={activeTab === 'chat' ? 'default' : 'ghost'}
              onClick={() => setActiveTab('chat')}
            >
              <MessageSquare className="h-4 w-4" />
              <span className="ml-2">Chat</span>
            </Button>
            <Button
              variant={activeTab === 'models' ? 'default' : 'ghost'}
              onClick={() => setActiveTab('models')}
            >
              <Settings className="h-4 w-4" />
              <span className="ml-2">Models</span>
            </Button>
          </div>
          <ServerStatus />
        </div>
      </div>

      <div className="flex-1 overflow-hidden">
        {activeTab === 'chat' ? <ChatInterface /> : <ModelManager />}
      </div>
    </div>
  )
} 