import { NextResponse } from 'next/server';
<<<<<<< HEAD
import fs from 'fs';
import path from 'path';
import { sanitizeFilename } from '@/app/(presentation-generator)/utils/others';

=======
import fs from 'fs/promises';
import path from 'path';
>>>>>>> 78e1006 (Initial: presenton)

export async function POST(request: Request) {
  try {
    const { filePath } = await request.json();
<<<<<<< HEAD
   
      const sanitizedFilePath = sanitizeFilename(filePath);
      const normalizedPath = path.normalize(sanitizedFilePath);
      const allowedBaseDirs = [
        process.env.APP_DATA_DIRECTORY || '/app/user_data',
        process.env.TEMP_DIRECTORY || '/tmp',
        '/app/user_data' 
      ];
      const resolvedPath = fs.realpathSync(path.resolve(normalizedPath));
      const isPathAllowed = allowedBaseDirs.some(baseDir => {
      const resolvedBaseDir = fs.realpathSync(path.resolve(baseDir));
      return resolvedPath.startsWith(resolvedBaseDir + path.sep) || resolvedPath === resolvedBaseDir;
    });
    if (!isPathAllowed) {
      console.error('Unauthorized file access attempt:', resolvedPath);
      return NextResponse.json(
        { error: 'Access denied: File path not allowed' },
        { status: 403 }
      );
    }
    const content=  fs.readFileSync(resolvedPath, 'utf-8');
=======

    // Validate file path
    if (!filePath || typeof filePath !== 'string') {
      return NextResponse.json(
        { error: 'Invalid file path' },
        { status: 400 }
      );
    }

    // Security check: ensure the path is within /tmp directory
    const normalizedPath = path.normalize(filePath);
    if (!normalizedPath.startsWith('/tmp/')) {
      return NextResponse.json(
        { error: 'Access denied: File must be in /tmp directory' },
        { status: 403 }
      );
    }

    // Read file content
    const content = await fs.readFile(normalizedPath, 'utf-8');
>>>>>>> 78e1006 (Initial: presenton)
    
    return NextResponse.json({ content });
  } catch (error) {
    console.error('Error reading file:', error);
    return NextResponse.json(
      { error: 'Failed to read file' },
      { status: 500 }
    );
  }
} 