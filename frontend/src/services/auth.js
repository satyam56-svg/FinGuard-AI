export function getToken() {
    return localStorage.getItem("finguard_token");
}

export function clearToken() {
    localStorage.removeItem("finguard_token");
}

export function isTokenExpired() {
    const payload = getTokenPayload();
    if (!payload || !payload.exp) {
        return true;
    }
    return Date.now() >= payload.exp * 1000;
}

export function getTokenPayload() {
    const token = getToken();

    if (!token) {
        return null;
    }

    try {
        const payload = token.split(".")[1];

        const decodedPayload = atob(
            payload
                .replace(/-/g, "+")
                .replace(/_/g, "/")
        );

        return JSON.parse(decodedPayload);
    } catch {
        return null;
    }
}

export function getCurrentUser() {
    if (isTokenExpired()) {
        clearToken();
        return null;
    }

    const payload = getTokenPayload();

    if (!payload) {
        return null;
    }

    return {
        username: payload.sub,
        role: payload.role,
    };
}

export function getUserRole() {
    return getTokenPayload()?.role || null;
}

export function isAuthenticated() {
    return Boolean(getToken()) && !isTokenExpired();
}