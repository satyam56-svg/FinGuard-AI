const API_BASE_URL = "http://127.0.0.1:8000";

function getAuthHeaders() {
    const token = localStorage.getItem("finguard_token");

    if (!token) {
        throw new Error("Authentication required.");
    }

    return {
        Authorization: `Bearer ${token}`,
    };
}

async function parseResponse(response, fallbackMessage) {
    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail
                ? typeof data.detail === "string"
                    ? data.detail
                    : JSON.stringify(data.detail)
                : fallbackMessage
        );
    }

    return data;
}


export async function registerUser(user) {
    const response = await fetch(
        `${API_BASE_URL}/auth/register`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(user),
        }
    );

    return parseResponse(
        response,
        "Registration failed."
    );
}


export async function loginUser(credentials) {
    const response = await fetch(
        `${API_BASE_URL}/auth/login`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(credentials),
        }
    );

    return parseResponse(
        response,
        "Login failed."
    );
}


export async function predictTransaction(transaction) {
    const response = await fetch(
        `${API_BASE_URL}/predict`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                ...getAuthHeaders(),
            },
            body: JSON.stringify(transaction),
        }
    );

    return parseResponse(
        response,
        "Prediction request failed."
    );
}


export async function getPredictionHistory() {
    const response = await fetch(
        `${API_BASE_URL}/predictions/history`,
        {
            method: "GET",
            headers: {
                ...getAuthHeaders(),
            },
        }
    );

    return parseResponse(
        response,
        "Unable to load prediction history."
    );
}


export async function getAnalystStats() {
    const response = await fetch(
        `${API_BASE_URL}/analyst/dashboard/stats`,
        {
            method: "GET",
            headers: {
                ...getAuthHeaders(),
            },
        }
    );

    return parseResponse(
        response,
        "Unable to load dashboard statistics."
    );
}


export async function getRiskDistribution() {
    const response = await fetch(
        `${API_BASE_URL}/analyst/dashboard/risk-distribution`,
        {
            method: "GET",
            headers: {
                ...getAuthHeaders(),
            },
        }
    );

    return parseResponse(
        response,
        "Unable to load risk distribution."
    );
}


export async function getRecentPredictions() {
    const response = await fetch(
        `${API_BASE_URL}/analyst/dashboard/recent-predictions`,
        {
            method: "GET",
            headers: {
                ...getAuthHeaders(),
            },
        }
    );

    return parseResponse(
        response,
        "Unable to load recent predictions."
    );
}


export async function getAdminUsers() {
    const response = await fetch(
        `${API_BASE_URL}/admin/users`,
        {
            method: "GET",
            headers: {
                ...getAuthHeaders(),
            },
        }
    );

    return parseResponse(
        response,
        "Unable to load users."
    );
}


export async function updateUserRole(userId, role) {
    const response = await fetch(
        `${API_BASE_URL}/admin/users/${userId}/role`,
        {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                ...getAuthHeaders(),
            },
            body: JSON.stringify({
                role,
            }),
        }
    );

    return parseResponse(
        response,
        "Unable to update user role."
    );
}


export async function updateUserStatus(userId, isActive) {
    const response = await fetch(
        `${API_BASE_URL}/admin/users/${userId}/status`,
        {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                ...getAuthHeaders(),
            },
            body: JSON.stringify({
                is_active: isActive,
            }),
        }
    );

    return parseResponse(
        response,
        "Unable to update user status."
    );
}


export async function checkHealth() {
    const response = await fetch(
        `${API_BASE_URL}/health`
    );

    if (!response.ok) {
        throw new Error(
            "Backend is unavailable."
        );
    }

    return response.json();
}