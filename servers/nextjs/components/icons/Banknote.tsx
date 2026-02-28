import { cn } from '@/lib/utils'
import React from 'react'

const BanknoteIcon = ({
    className
}: {
    className?: string
}) => {
    return (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" height="40" viewBox="0 0 40 40" width="40" className={cn(className)}>
            <path d="M20 21a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z" fill="currentColor" />
            <path d="M8 17a4.001 4.001 0 0 0 3.874-3h16.252c.445 1.725 2.01 3 3.874 3v5a4.001 4.001 0 0 0-3.874 3H11.874A4.001 4.001 0 0 0 8 22v-5Zm12 5a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5Z" fill="currentColor" />
            <path d="M4 11a1 1 0 0 1 1-1h30a1 1 0 0 1 1 1v17a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V11Zm6.959 2.498a3 3 0 0 1-3.27 2.486c-.344-.036-.689.207-.689.552v5.928c0 .345.345.588.688.552a3 3 0 0 1 3.27 2.486c.046.273.266.498.542.498h17c.276 0 .496-.226.541-.498a3 3 0 0 1 3.27-2.486c.344.036.689-.207.689-.552v-5.928c0-.345-.345-.588-.688-.552a3 3 0 0 1-3.27-2.486c-.046-.272-.266-.498-.542-.498h-17c-.276 0-.496.226-.541.498Z" fill="currentColor" />
        </svg>
    )
}

export default BanknoteIcon 