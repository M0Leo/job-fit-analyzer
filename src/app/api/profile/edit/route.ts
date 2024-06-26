import { editProfile } from "@/lib/actions/profile";
import { currentUser } from "@/lib/auth";
import { editProfileSchema } from "@/lib/schemas";
import { NextRequest, NextResponse } from "next/server";

export async function PUT(req: NextRequest) {
  const user = await currentUser();
  if (!user) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }
  const body = await req.json();
  const validated = editProfileSchema.safeParse(body);

  if (!validated.success) {
    return NextResponse.json({ error: "Invalid input" }, { status: 400 });
  }

  const { bio, location, website, resume } = validated.data;

  const profile = await editProfile(user.id!!, { bio, location, website, resume });
  if (!profile) {
    return NextResponse.json({ error: "Failed to update profile" }, { status: 500 });
  }

  return NextResponse.json({ success: true, profile }, { status: 200 });
}
