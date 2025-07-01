"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

const hasLowercase = (password: string) => /[a-z]/.test(password);
const hasUppercase = (password: string) => /[A-Z]/.test(password);
const hasDigit = (password: string) => /\d/.test(password);
const hasSpecialChar = (password: string) => /[^a-zA-Z0-9]/.test(password);


type RegisterFormProps = {
  onSuccess?: () => void;
};

const isAlphanumeric = (str: string): boolean => {
  for (let i = 0; i < str.length; i++) {
    const code = str.charCodeAt(i);
    if (
      !(code > 47 && code < 58) &&   // numeric (0-9)
      !(code > 64 && code < 91) &&   // upper alpha (A-Z)
      !(code > 96 && code < 123)     // lower alpha (a-z)
    ) {
      return false;
    }
  }
  return str.length > 0;
};

export default function RegisterForm({ onSuccess }: RegisterFormProps) {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const router = useRouter();


  const validate = () => {
    const newErrors: Record<string, string> = {};

    // Username validation
    if (!formData.username.trim()) {
      newErrors.username = "Username is required";
    } else if (!isAlphanumeric(formData.username)) {
      newErrors.username = "Username can only contain letters and numbers";
    } else if (formData.username.length < 5 || formData.username.length > 20) {
      newErrors.username = "Username must be between 5-20 characters";
    }

    // Password validation
    if (!formData.password) {
      newErrors.password = "Password is required";
    } else if (formData.password.length < 8 || formData.password.length > 20) {
      newErrors.password = "Password must be between 8-20 characters";
    } else if (
        !hasLowercase(formData.password) ||
        !hasUppercase(formData.password) ||
        !hasDigit(formData.password) ||
        !hasSpecialChar(formData.password)
    ) {
      newErrors.password =
        "Password must contain at least one uppercase, one lowercase, one number and one special character";
    }

    // Email validation
    if (!formData.email.trim()) {
      newErrors.email = "Email is required";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = "Invalid email format";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validate()) return;

    setIsSubmitting(true);
    try {
      const response = await fetch("/api/v1/auth/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Registration failed");
      }

      onSuccess ? onSuccess() : router.push("/");
    } catch (error) {
      setErrors({ submit: error instanceof Error ? error.message : "Registration failed" });
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {errors.submit && (
        <div className="text-red-500 text-sm">{errors.submit}</div>
      )}

      <div>
        <label htmlFor="username" className="block text-sm font-medium">
          Username
        </label>
        <input
          type="text"
          id="username"
          name="username"
          value={formData.username}
          onChange={handleChange}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
        />
        {errors.username && (
          <p className="mt-1 text-sm text-red-500">{errors.username}</p>
        )}
      </div>

      <div>
        <label htmlFor="email" className="block text-sm font-medium">
          Email
        </label>
        <input
          type="email"
          id="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
        />
        {errors.email && (
          <p className="mt-1 text-sm text-red-500">{errors.email}</p>
        )}
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium">
          Password
        </label>
        <input
          type="password"
          id="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
        />
        {errors.password && (
          <p className="mt-1 text-sm text-red-500">{errors.password}</p>
        )}
      </div>

      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
      >
        {isSubmitting ? "Registering..." : "Register"}
      </button>
    </form>
  );
}
