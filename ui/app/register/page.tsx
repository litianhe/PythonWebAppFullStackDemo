"use client";

import { useRouter } from "next/navigation";
import RegisterForm from "../components/auth/RegisterForm";

export default function RegisterPage() {
  const router = useRouter();

  const handleSuccess = () => {
    router.push("/");
  };

  return (
    <div className="max-w-md mx-auto py-8">
      <h1 className="text-2xl font-bold mb-6">Register</h1>
      <RegisterForm onSuccess={handleSuccess} />
    </div>
  );
}
