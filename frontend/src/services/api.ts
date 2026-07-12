const API_URL =
  import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000/api";

export async function apiRequest<T>(
  path: string,
  options?: RequestInit
): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });

  if (!response.ok) {
    let message = `API request failed with status ${response.status}`;

    try {
      const body = (await response.json()) as {
        detail?: string;
      };

      if (body.detail) {
        message = body.detail;
      }
    } catch {
      // The response did not contain JSON.
    }

    throw new Error(message);
  }

  return response.json() as Promise<T>;
}