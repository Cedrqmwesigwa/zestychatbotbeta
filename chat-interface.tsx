import React, { useState } from 'react'
import { ArrowLeft, Camera, Mic, Send } from 'lucide-react'
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

export default function Component() {
  const [messages, setMessages] = useState([
    { type: 'user', content: 'Saphire rx 580' },
    { type: 'bot', content: "The Sapphire Radeon RX 580 is a popular mid-range graphics card released in 2017. It's based on AMD's Polaris architecture and offers excellent performance for gaming at 1080p and even 1440p resolutions.\n\nKey features and specifications:\n\n• Architecture: Polaris 20" }
  ])
  const [input, setInput] = useState('')

  const handleSend = () => {
    if (input.trim()) {
      setMessages([...messages, { type: 'user', content: input }])
      setInput('')
      // Here you would typically call your API to get the bot's response
    }
  }

  return (
    <div className="flex flex-col h-screen bg-gray-900 text-white">
      <header className="flex justify-between items-center p-4 border-b border-gray-700">
        <ArrowLeft className="w-6 h-6" />
        <Avatar className="w-8 h-8">
          <AvatarImage src="/placeholder.svg" />
          <AvatarFallback>AI</AvatarFallback>
        </Avatar>
      </header>
      <main className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message, index) => (
          <div key={index} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[70%] p-3 rounded-2xl ${message.type === 'user' ? 'bg-blue-600' : 'bg-gray-700'}`}>
              <p className="text-sm">{message.content}</p>
            </div>
          </div>
        ))}
      </main>
      <footer className="p-4 border-t border-gray-700">
        <div className="flex items-center space-x-2">
          <Input
            className="flex-1 bg-gray-800 border-none text-white placeholder-gray-400"
            placeholder="Type, talk or send..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
          <Button size="icon" variant="ghost">
            <Mic className="w-5 h-5 text-blue-400" />
          </Button>
          <Button size="icon" variant="ghost">
            <Camera className="w-5 h-5 text-blue-400" />
          </Button>
          <Button size="icon" variant="ghost" onClick={handleSend}>
            <Send className="w-5 h-5 text-blue-400" />
          </Button>
        </div>
        <p className="text-xs text-gray-400 mt-2 text-center">Zesty</p>
      </footer>
    </div>
  )
}