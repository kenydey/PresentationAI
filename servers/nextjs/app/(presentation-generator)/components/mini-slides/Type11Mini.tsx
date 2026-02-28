import { RootState } from '@/store/store';
import React from 'react'
import { useSelector } from 'react-redux';

type Type11MiniProps = {
    title: string;
    description?: string;
    infographics: {
        title: string;
        description: string;
        chart: {
            chart_type: string;
            value: {
                number_type: string;
                numerical: number;
                suffix: string;
            }
        }
    }[];
}

const Type11Mini = ({ title, description, infographics }: Type11MiniProps) => {
    const { currentColors } = useSelector((state: RootState) => state.theme);

    return (
        <div className='w-full aspect-video bg-white rounded-lg p-4 flex flex-col items-center justify-center slide-container'>
            <div className="text-center mb-4">
                <p className='text-[8px] slide-title font-semibold'>{title}</p>
                {description && <p className='text-[6px] slide-description'>{description}</p>}
            </div>
            <div style={{ gridTemplateColumns: `repeat(${infographics.length}, 1fr)` }} className='grid justify-center w-full gap-2'>
                {infographics.map((item, index) => (
                    <div key={index} className={`bg-gray-50 slide-box rounded p-1 text-center ${infographics.length === 1 ? 'max-w-[100px] mx-auto' : ''}`}>
                        <div className="w-8 h-8 rounded-full  flex-col mx-auto mb-1 flex items-center justify-center"
                            style={{ backgroundColor: currentColors.iconBg }}
                        >
                            <p className='text-[10px] text-white'>{item.chart.value.numerical}</p>
                        </div>
                        <p className='text-[8px] font-medium slide-heading'>{item.title}</p>
                    </div>
                ))}
            </div>
        </div>
    )
}

export default Type11Mini
