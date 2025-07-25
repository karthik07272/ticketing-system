import { apiUrl } from "../config/env.js"

const API_BASE_URL = apiUrl

class TicketService {
  async searchTickets(params) {
    const queryParams = new URLSearchParams()

    Object.entries(params).forEach(([key, value]) => {
      if (value !== "" && value !== null && value !== undefined) {
        queryParams.append(key, value)
      }
    })

    try {
      const res = await fetch(`${API_BASE_URL}/search-tickets?${queryParams}`)
      if (!res.ok) {
        const { detail } = await res.json().catch(() => ({}))
        throw new Error(detail || `Request failed with status ${res.status}`)
      }
      return res.json()
    } catch (err) {
      console.error(err)
      throw new Error("Unable to reach the ticket API. Please check your server is running.")
    }
  }

  async getTicketById(id) {
    const response = await fetch(`${API_BASE_URL}/get-ticket-by-id?id=${id}`)
    if (!response.ok) {
      throw new Error("Failed to fetch ticket")
    }
    return response.json()
  }

  async createTicket(ticketData) {
    const response = await fetch(`${API_BASE_URL}/create-ticket`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(ticketData),
    })
    if (!response.ok) {
      throw new Error("Failed to create ticket")
    }
    return response.json()
  }

  async updateTicket(id, ticketData) {
    const response = await fetch(`${API_BASE_URL}/update-ticket?id=${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(ticketData),
    })
    if (!response.ok) {
      throw new Error("Failed to update ticket")
    }
    return response.json()
  }

  async deleteTicket(id) {
    const response = await fetch(`${API_BASE_URL}/delete-ticket?id=${id}`, {
      method: "DELETE",
    })
    if (!response.ok) {
      throw new Error("Failed to delete ticket")
    }
    return response.json()
  }

  async seedDatabase(count = 100000) {
    const response = await fetch(`${API_BASE_URL}/seed-database?count=${count}`, {
      method: "POST",
    })
    if (!response.ok) {
      throw new Error("Failed to seed database")
    }
    return response.json()
  }
}

export const ticketService = new TicketService()
