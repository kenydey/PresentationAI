import { NextRequest, NextResponse } from "next/server";
import { getDb } from "../../(presentation-generator)/services/db";

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const userId = searchParams.get("userId");

    if (!userId) {
      return NextResponse.json(
        { error: "User ID is required" },
        { status: 400 }
      );
    }

    const db = await getDb();
    const result = await db.get(
      "SELECT data FROM settings WHERE key = 'theme' AND userId = ?",
      userId
    );
    await db.close();

    if (result) {
      return NextResponse.json({ theme: JSON.parse(result.data) });
    }

    return NextResponse.json({ theme: null });
  } catch (error) {
    console.error("Error retrieving theme:", error);
    return NextResponse.json(
      { error: "Failed to retrieve theme" },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { userId, themeData } = body;

    if (!userId || !themeData) {
      return NextResponse.json(
        { error: "User ID and theme data are required" },
        { status: 400 }
      );
    }

    const db = await getDb();
    const themeDataJson = JSON.stringify(themeData);

    await db.run(
      `INSERT OR REPLACE INTO settings (key, userId, data, updated_at) 
       VALUES ('theme', ?, ?, CURRENT_TIMESTAMP)`,
      [userId, themeDataJson]
    );

    await db.close();

    return NextResponse.json({ success: true });
  } catch (error) {
    console.error("Error saving theme:", error);
    return NextResponse.json(
      { error: "Failed to save theme" },
      { status: 500 }
    );
  }
}
