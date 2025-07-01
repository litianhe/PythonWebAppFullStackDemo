"use client";

import { useState } from "react";

type CommentFormProps = {
  parentId?: number;
  onSuccess?: () => void;
};

export default function CommentForm({ parentId, onSuccess }: CommentFormProps) {
  const [content, setContent] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");

  const remainingChars = 200 - content.length;
  const isValid = content.length >= 3 && content.length <= 200;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!isValid) return;

    setIsSubmitting(true);
    try {
      const token = localStorage.getItem("access_token") || sessionStorage.getItem("access_token");
      if (!token) {
        throw new Error("Please login to post comments");
      }

      const response = await fetch("/api/v1/comments/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({
          content,
          parent_id: parentId,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to post comment");
      }

      setContent("");
      setError("");
      if (onSuccess) onSuccess();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to post comment");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-2">
      <div>
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="Write your comment..."
          className="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 min-h-[100px]"
          maxLength={200}
        />
        <div className="flex justify-between">
          <span
            className={`text-xs ${
              remainingChars < 20 ? "text-red-500" : "text-gray-500"
            }`}
          >
            {remainingChars} characters remaining
          </span>
          {content.length > 0 && content.length < 3 && (
            <span className="text-xs text-red-500">
              Minimum 3 characters required
            </span>
          )}
        </div>
      </div>

      {error && <div className="text-red-500 text-sm">{error}</div>}

      <button
        type="submit"
        disabled={!isValid || isSubmitting}
        className="inline-flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {isSubmitting ? "Posting..." : "Post Comment"}
      </button>
    </form>
  );
}
