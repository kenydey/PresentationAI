'use client';
import { ArrowLeftIcon } from '@radix-ui/react-icons'
import React from 'react'
import { useRouter } from 'next/navigation';

const BackBtn = () => {
    const router = useRouter();
    return (
<<<<<<< HEAD
        <button onClick={() => router.back()} className='bg-white-900 border border-white/20 hover:border-white/60 transition-all duration-200 rounded-full p-2'>
            <ArrowLeftIcon className="w-5 h-5 text-white" />
=======
        <button onClick={() => router.back()} className='bg-white rounded-full p-2'>
            <ArrowLeftIcon className="w-5 h-5 text-black" />
>>>>>>> 78e1006 (Initial: presenton)
        </button>
    )
}

export default BackBtn
