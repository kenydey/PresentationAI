import { Trash2 } from 'lucide-react';
import React from 'react'

interface NewSlideProps {
    onSelectLayout: (type: number) => void;
    setShowNewSlideSelection: (show: boolean) => void;
}

const LayoutPreview = ({ type }: { type: string }) => {
    switch (type) {
        case 'type1':
            return (
                <div className="w-full h-[120px] bg-white p-3 flex items-center gap-2">
                    <div className="w-1/2 space-y-1.5">
                        <div className="h-3 bg-gray-200 w-3/4"></div>
                        <div className="h-2 bg-gray-100 w-3/4"></div>
                    </div>
                    <div className="w-1/2 h-full bg-gray-100 flex items-center justify-center">
                        <p className='text-gray-500 text-sm'>image</p>
                    </div>
                </div>
            )
        case 'type2':
            return (
                <div className="w-full h-[120px] bg-white p-3 flex flex-col gap-2">
                    <div className="h-3 bg-gray-200 w-1/2 mx-auto"></div>
                    <div className="flex gap-2 flex-1">
                        {[1, 2, 3].map((i) => (
                            <div key={i} className="flex-1 bg-gray-100 p-1.5">
                                <div className="h-2 bg-gray-200 w-3/4 mb-1"></div>
                                <div className="h-1.5 bg-gray-50 w-full"></div>
                            </div>
                        ))}
                    </div>
                </div>
            )
        case 'type4':
            return (
                <div className="w-full h-[120px] bg-white p-3 flex flex-col gap-2">
                    <div className="h-3 bg-gray-200 w-1/2 mx-auto"></div>
                    <div className="grid grid-cols-3 gap-2 flex-1">
                        {[1, 2, 3].map((i) => (
                            <div key={i} className="bg-gray-100 p-1.5">
                                <div className="h-8 bg-gray-200 mb-1 flex items-center justify-center">
                                    <p className='text-gray-500 text-xs'>image</p>
                                </div>
                                <div className="h-1.5 bg-gray-50 w-3/4"></div>
                            </div>
                        ))}
                    </div>
                </div>
            )
        case 'type5':
            return (
                <div className="w-full h-[120px] bg-white p-3 flex flex-col  gap-2">
                    <div className="h-2 bg-gray-200 w-1/2 "></div>
                    <div className="w-full grid grid-cols-2 h-full items-center gap-2">
                        <div className=" bg-gray-100 h-full w-full flex items-center justify-center">
                            <p className='text-gray-500 text-xs'>chart</p>
                        </div>
                        <div className="h-4 bg-gray-100 w-full"></div>
                    </div>
                </div>
            )
        case 'type6':
            return (
                <div className="w-full h-[120px] bg-white p-3 flex gap-2">
                    <div className="w-1/2 space-y-1.5">
                        <div className="h-3 bg-gray-200 w-3/4"></div>
                        <div className="h-2 bg-gray-100 w-full"></div>
                    </div>
                    <div className="w-1/2 space-y-1.5">
                        {[1, 2].map((i) => (
                            <div key={i} className="flex gap-1.5 bg-gray-50 p-1.5">
                                <div className="w-4 h-4 bg-gray-200 rounded-full flex-shrink-0"></div>
                                <div className="flex-1">
                                    <div className="h-1.5 bg-gray-200 w-3/4"></div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )
        case 'type7':
            return (
                <div className="w-full h-[120px] bg-white p-3 flex flex-col gap-2">
                    <div className="h-3 bg-gray-200 w-1/2 mx-auto"></div>
                    <div className="flex justify-between px-6">
                        {[1, 2, 3].map((i) => (
                            <div key={i} className="text-center bg-gray-100 h-full flex flex-col items-center justify-center">
                                <div className="w-4 h-4 bg-gray-50 rounded-full flex items-center justify-center mx-auto mb-1">
                                    <p className='text-gray-500 text-xs'>Icon</p>
                                </div>
                                <div className="h-1.5 bg-gray-200 w-12 mb-1"></div>
                                <div className="h-5 bg-gray-200 w-12"></div>
                            </div>
                        ))}
                    </div>
                </div>
            )
        case 'type8':
            return (
                <div className="w-full h-[120px] bg-white p-3 flex gap-2">
                    <div className="w-1/2 space-y-1.5">
                        <div className="h-3 bg-gray-200 w-3/4"></div>
                        <div className="h-2 bg-gray-100 w-full"></div>
                    </div>
                    <div className="w-1/2 space-y-2">
                        {[1, 2].map((i) => (
                            <div key={i} className="flex gap-1.5 bg-gray-50 p-1.5">
                                <div className="w-6 h-6 bg-gray-200 flex-shrink-0 flex items-center justify-center">
                                    <p className='text-gray-500 text-[10px]'>Icon</p>
                                </div>
                                <div className="flex-1">
                                    <div className="h-1.5 bg-gray-200 w-3/4"></div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )
        case 'type9':
            return (
                <div className="w-full h-[120px] bg-white p-3 flex  gap-2">
                    <div className="w-1/2 space-y-1.5">
                        <div className="h-2 bg-gray-200 w-3/4"></div>
                        <div className="flex-1 bg-gray-100 h-full flex items-center justify-center">
                            <p className='text-gray-500 text-sm'>chart</p>
                        </div>
                    </div>
                    <div className="w-1/2 space-y-1.5">
                        {[1, 2, 3].map((i) => (
                            <div key={i} className="flex gap-1.5 bg-gray-50 p-1.5">
                                <div className="w-4 h-4 bg-gray-200 rounded-full flex-shrink-0"></div>
                                <div className="flex-1">
                                    <div className="h-1.5 bg-gray-200 w-3/4"></div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )
        case 'type10':
            return (
                <div className="w-full h-[120px] bg-white p-3 flex flex-col gap-2">
                    <div className="h-3 bg-gray-200 w-1/2 mx-auto"></div>
                    <div className="flex justify-center gap-8 flex-1">
                        {[1, 2].map((i) => (
                            <div key={i} className="text-center flex flex-col items-center">
                                <div className="w-12 h-12 rounded-full border-4  border-blue-200 flex items-center justify-center">

                                    <div className="text-xs text-gray-500">{i * 10}%</div>
                                </div>
                                <div className="h-2 bg-gray-200 w-24 mt-2"></div>
                                <div className="h-1.5 bg-gray-100 w-20 mt-1"></div>
                            </div>
                        ))}
                    </div>
                </div>
            )
        case 'type11':
            return (
                <div className="w-full h-[120px] bg-white p-3 flex flex-col gap-2">
                    <div className="h-3 bg-gray-200 w-1/2 mx-auto"></div>
                    <div className="flex justify-between gap-4 flex-1">
                        {[1, 2].map((i) => (
                            <div key={i} className="flex-1 bg-gray-50 p-2 rounded flex flex-col items-center">
                                <div className="w-10 h-10 rounded-full bg-blue-200 flex items-center justify-center mb-2">
                                    <div className="text-xs text-gray-500">257</div>
                                </div>
                                <div className="h-2 bg-gray-200 w-3/4 mb-1"></div>
                                <div className="h-1.5 bg-gray-100 w-2/3"></div>
                            </div>
                        ))}
                    </div>
                </div>
            )
        case 'type12':
            return (
                <div className="w-full h-[120px] bg-white p-3 flex justify-between gap-4">
                    <div className="w-1/2 flex flex-col justify-center space-y-2">
                        <div className="h-3 bg-gray-200 w-3/4"></div>
                        <div className="h-2 bg-gray-100 w-full"></div>
                    </div>
                    <div className="w-1/2 flex justify-center items-center">
                        <div className="w-16 h-16 rounded-full border-4 border-t-blue-200 border-r-blue-200 border-b-gray-50 border-l-gray-50 flex items-center justify-center">
                            <div className="w-4 h-4 text-xs ">Icon</div>
                        </div>
                    </div>
                </div>
            )
        case 'type13':
            return (
                <div className="w-full h-[120px] bg-white p-3 flex flex-col gap-2">
                    <div className="text-center space-y-1">
                        <div className="h-3 bg-gray-200 w-1/2 mx-auto"></div>
                        <div className="h-2 bg-gray-100 w-3/4 mx-auto"></div>
                    </div>
                    <div className="flex justify-center gap-12 flex-1">
                        {[1, 2].map((i) => (
                            <div key={i} className="text-center flex flex-col items-center">
                                <div className="w-12 h-12 rounded-full border-4 border-t-blue-200 border-r-blue-200 border-b-gray-50 border-l-gray-50 flex items-center justify-center mb-1">
                                    <div className="text-xs ">Icon</div>
                                </div>
                                <div className="h-2 bg-gray-200 w-32 mb-1"></div>
                                <div className="h-1.5 bg-gray-100 w-24"></div>
                            </div>
                        ))}
                    </div>
                </div>
            )
        case 'type14':
            return (
                <div className="w-full h-[120px] bg-white p-3 flex flex-col gap-2">
                    <div className="text-center space-y-1">
                        <div className="h-3 bg-gray-200 w-1/2 mx-auto"></div>
                        <div className="h-2 bg-gray-100 w-3/4 mx-auto"></div>
                    </div>
                    <div className="flex justify-center gap-6 flex-1">
                        {[1, 2].map((i) => (
                            <div key={i} className="flex-1 bg-gray-50 p-2 rounded flex flex-col items-center">
                                <div className="relative w-16 h-10">
                                    <svg width="64" height="40" viewBox="0 0 64 40">
                                        <path
                                            d="M 4,36 A 28,28 0 0 1 60,36"
                                            fill="none"
                                            stroke="#4895ef"
                                            strokeWidth="6"
                                            strokeLinecap="round"
                                        />
                                        <text
                                            x="32"
                                            y="28"
                                            dominantBaseline="middle"
                                            textAnchor="middle"
                                            fontSize="12"
                                            fontWeight="500"
                                            fill="#4895ef"
                                        >
                                            {i === 1 ? '30%' : '80%'}
                                        </text>
                                    </svg>
                                </div>
                                <div className="h-2 bg-gray-200 w-3/4 mb-1 mt-2"></div>
                                <div className="h-1.5 bg-gray-100 w-2/3 text-center"></div>
                            </div>
                        ))}
                    </div>
                </div>
            )
        case 'type15':
            return (
                <div className="w-full h-[120px] bg-white p-3 flex flex-col gap-2">
                    <div className="text-center space-y-1">
                        <div className="h-3 bg-gray-200 w-1/2 mx-auto"></div>
                        <div className="h-2 bg-gray-100 w-3/4 mx-auto"></div>
                    </div>
                    <div className="flex justify-center gap-6 flex-1">
                        {[1, 2].map((i) => (
                            <div key={i} className="flex-1 bg-white shadow-sm rounded-lg p-2 flex flex-col items-center">
                                <div className="relative w-16 h-10">
                                    <svg width="64" height="40" viewBox="0 0 64 40">
                                        <path
                                            d="M 4,36 A 28,28 0 0 1 60,36"
                                            fill="none"
                                            stroke="#4895ef"
                                            strokeWidth="6"
                                            strokeLinecap="round"
                                        />
                                        <g transform={`rotate(${i === 1 ? '-60' : '-20'} 32 36)`}>
                                            <line
                                                x1="32"
                                                y1="36"
                                                x2="32"
                                                y2="14"
                                                stroke="#4895ef"
                                                strokeWidth="2"
                                                strokeLinecap="round"
                                            />
                                        </g>
                                    </svg>
                                </div>
                                <div className="h-2 bg-gray-200 w-3/4 mb-1 mt-2"></div>
                                <div className="h-1.5 bg-gray-100 w-2/3 text-center"></div>
                            </div>
                        ))}
                    </div>
                </div>
            )
        case 'type16':
            return (
                <div className="w-full h-[120px] bg-white p-3 flex flex-col gap-2">
                    <div className="text-center space-y-1">
                        <div className="h-3 bg-gray-200 w-1/2 mx-auto"></div>
                        <div className="h-2 bg-gray-100 w-3/4 mx-auto"></div>
                    </div>
                    <div className="flex justify-center gap-6 flex-1">
                        {[1, 2].map((i) => (
                            <div key={i} className="flex-1 bg-white shadow-sm rounded-lg p-3 flex flex-col">
                                <div className="h-2 w-full bg-gray-100 rounded-full mb-2">
                                    <div
                                        className={`h-full ${i === 1 ? 'w-2/3' : 'w-3/5'} bg-blue-300 rounded-full`}
                                    ></div>
                                </div>
                                <div className="h-2 bg-gray-200 w-3/4 mb-1"></div>
                                <div className="h-1.5 bg-gray-100 w-full text-center"></div>
                            </div>
                        ))}
                    </div>
                </div>
            )
        default:
            return null
    }
}

const NewSlide = ({ onSelectLayout, setShowNewSlideSelection }: NewSlideProps) => {
    return (
        <div className='my-6 w-full bg-gray-50 p-8 max-w-[1280px]'>
            <div className='flex justify-between items-center  mb-8'>

                <h2 className="text-2xl font-semibold">Select a Slide Layout</h2>
                <Trash2 onClick={() => setShowNewSlideSelection(false)} className='text-gray-500 text-2xl cursor-pointer' />
            </div>
            <div className='grid grid-cols-4 gap-4'>
                {['type1', 'type2', 'type4', 'type5', 'type6', 'type7', 'type8', 'type9', 'type10', 'type11', 'type12', 'type13', 'type14', 'type15', 'type16'].map((type) => (
                    <div
                        key={type}
                        className="transform hover:scale-105 transition-transform cursor-pointer"
                        onClick={() => onSelectLayout(parseInt(type.replace('type', '')))}
                    >
                        <div className="bg-white rounded-lg shadow-sm overflow-hidden">
                            <div className="p-2 border-b">
                                <h3 className="text-xs font-medium">Layout {type.replace('type', '')}</h3>
                            </div>
                            <div className="p-2">
                                <LayoutPreview type={type} />
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    )
}

export default NewSlide
