"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Camera, Users, Shield, AlertTriangle, Eye, Settings } from "lucide-react"
import Link from "next/link"

export default function HomePage() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [stats, setStats] = useState({
    activeCameras: 0,
    detectedPeople: 0,
    alerts: 0,
    uptime: "0%",
  })

  useEffect(() => {
    // Check authentication status
    const token = localStorage.getItem("auth_token")
    setIsAuthenticated(!!token)

    // Load stats
    if (token) {
      fetchStats()
    }
  }, [])

  const fetchStats = async () => {
    try {
      const response = await fetch("/api/stats")
      if (response.ok) {
        const data = await response.json()
        setStats(data)
      }
    } catch (error) {
      console.error("Error fetching stats:", error)
    }
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
        <div className="max-w-4xl w-full">
          {/* Hero Section */}
          <div className="text-center mb-12">
            <div className="flex items-center justify-center mb-6">
              <Shield className="h-16 w-16 text-blue-600 mr-4" />
              <h1 className="text-4xl font-bold text-gray-900">Sistema de Detección Facial</h1>
            </div>
            <p className="text-xl text-gray-600 mb-8">
              Tecnología avanzada de IA para seguridad y monitoreo en tiempo real
            </p>
            <div className="flex gap-4 justify-center">
              <Link href="/login">
                <Button size="lg" className="bg-blue-600 hover:bg-blue-700">
                  Iniciar Sesión
                </Button>
              </Link>
              <Link href="/register">
                <Button size="lg" variant="outline">
                  Registrarse
                </Button>
              </Link>
            </div>
          </div>

          {/* Features Grid */}
          <div className="grid md:grid-cols-3 gap-6 mb-12">
            <Card>
              <CardHeader>
                <Camera className="h-8 w-8 text-blue-600 mb-2" />
                <CardTitle>Detección en Tiempo Real</CardTitle>
                <CardDescription>Monitoreo continuo con múltiples cámaras simultáneas</CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <Users className="h-8 w-8 text-green-600 mb-2" />
                <CardTitle>Reconocimiento Facial</CardTitle>
                <CardDescription>Identificación precisa de personas autorizadas y desconocidas</CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <AlertTriangle className="h-8 w-8 text-orange-600 mb-2" />
                <CardTitle>Alertas Inteligentes</CardTitle>
                <CardDescription>Notificaciones automáticas por email ante eventos importantes</CardDescription>
              </CardHeader>
            </Card>
          </div>

          {/* Mission & Vision */}
          <div className="grid md:grid-cols-2 gap-8">
            <Card>
              <CardHeader>
                <CardTitle className="text-blue-600">Nuestra Misión</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600">
                  Proporcionar soluciones de seguridad inteligentes y accesibles que protejan espacios y personas
                  mediante tecnología de vanguardia en detección facial y análisis de video.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-green-600">Nuestra Visión</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600">
                  Ser líderes en innovación de sistemas de seguridad basados en IA, creando un mundo más seguro y
                  conectado donde la tecnología sirva para proteger lo que más importa.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <Shield className="h-8 w-8 text-blue-600 mr-3" />
              <h1 className="text-xl font-semibold text-gray-900">Sistema de Detección Facial</h1>
            </div>
            <nav className="flex items-center space-x-4">
              <Link href="/dashboard">
                <Button variant="ghost">Dashboard</Button>
              </Link>
              <Link href="/cameras">
                <Button variant="ghost">Cámaras</Button>
              </Link>
              <Link href="/events">
                <Button variant="ghost">Eventos</Button>
              </Link>
              <Link href="/profile">
                <Button variant="ghost">Perfil</Button>
              </Link>
              <Button
                variant="outline"
                onClick={() => {
                  localStorage.removeItem("auth_token")
                  setIsAuthenticated(false)
                }}
              >
                Cerrar Sesión
              </Button>
            </nav>
          </div>
        </div>
      </header>

      {/* Dashboard Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Cámaras Activas</CardTitle>
              <Camera className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.activeCameras}</div>
              <Badge variant="secondary" className="mt-1">
                En línea
              </Badge>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Personas Detectadas</CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.detectedPeople}</div>
              <p className="text-xs text-muted-foreground">Hoy</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Alertas</CardTitle>
              <AlertTriangle className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.alerts}</div>
              <p className="text-xs text-muted-foreground">Últimas 24h</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Tiempo Activo</CardTitle>
              <Eye className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.uptime}</div>
              <p className="text-xs text-muted-foreground">Sistema</p>
            </CardContent>
          </Card>
        </div>

        {/* Quick Actions */}
        <div className="grid md:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle>Acciones Rápidas</CardTitle>
              <CardDescription>Gestiona tu sistema de seguridad</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <Link href="/cameras">
                <Button className="w-full justify-start bg-transparent" variant="outline">
                  <Camera className="mr-2 h-4 w-4" />
                  Ver Cámaras en Vivo
                </Button>
              </Link>
              <Link href="/events">
                <Button className="w-full justify-start bg-transparent" variant="outline">
                  <AlertTriangle className="mr-2 h-4 w-4" />
                  Revisar Eventos
                </Button>
              </Link>
              <Link href="/settings">
                <Button className="w-full justify-start bg-transparent" variant="outline">
                  <Settings className="mr-2 h-4 w-4" />
                  Configuración
                </Button>
              </Link>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Estado del Sistema</CardTitle>
              <CardDescription>Monitoreo en tiempo real</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm">Detección Facial</span>
                  <Badge variant="default">Activo</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">Notificaciones Email</span>
                  <Badge variant="default">Activo</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">Base de Datos</span>
                  <Badge variant="default">Conectada</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">Almacenamiento</span>
                  <Badge variant="secondary">85% Libre</Badge>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  )
}
