import { type NextRequest, NextResponse } from "next/server"
import bcrypt from "bcryptjs"

// Simulación de base de datos en memoria
const users = [
  {
    id: 1,
    email: "admin@empresa.com",
    password: "$2a$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi",
    companyName: "Empresa Demo",
    contactName: "Administrador",
  },
]

export async function POST(request: NextRequest) {
  try {
    const { companyName, contactName, email, password } = await request.json()

    if (!companyName || !contactName || !email || !password) {
      return NextResponse.json({ message: "Todos los campos son requeridos" }, { status: 400 })
    }

    // Verificar si el email ya existe
    const existingUser = users.find((u) => u.email === email)
    if (existingUser) {
      return NextResponse.json({ message: "El email ya está registrado" }, { status: 409 })
    }

    // Hashear contraseña
    const hashedPassword = await bcrypt.hash(password, 10)

    // Crear nuevo usuario
    const newUser = {
      id: users.length + 1,
      email,
      password: hashedPassword,
      companyName,
      contactName,
    }

    users.push(newUser)

    return NextResponse.json({
      message: "Usuario registrado exitosamente",
      user: {
        id: newUser.id,
        email: newUser.email,
        companyName: newUser.companyName,
        contactName: newUser.contactName,
      },
    })
  } catch (error) {
    console.error("Register error:", error)
    return NextResponse.json({ message: "Error interno del servidor" }, { status: 500 })
  }
}
