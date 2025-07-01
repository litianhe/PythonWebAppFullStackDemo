"use client";

import { useRouter } from "next/navigation";
import LoginForm from "../components/auth/LoginForm";

export default function LoginPage() {
  const router = useRouter();

  const handleSuccess = () => {
    router.push("/");
  };

  return (
    <div className="max-w-md mx-auto py-8">
      <h1 className="text-2xl font-bold mb-6">Login</h1>
      <LoginForm onSuccess={handleSuccess} />
    </div>
  );
}
