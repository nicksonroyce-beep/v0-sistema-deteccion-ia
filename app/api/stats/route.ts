import { NextResponse } from "next/server"

export async function GET() {
  try {
    // Simulación de estadísticas del sistema
    const stats = {
      activeCameras: 3,
      detectedPeople: 12,
      alerts: 2,
      uptime: "99.8%",
    }

    return NextResponse.json(stats)
  } catch (error) {
    console.error("Stats error:", error)
    return NextResponse.json({ message: "Error al obtener estadísticas" }, { status: 500 })
  }
}
