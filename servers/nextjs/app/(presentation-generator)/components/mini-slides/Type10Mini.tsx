import React from 'react'
import AllInfoGraphics from '../info_graphics/AllInfoGraphics';
import MiniInfoGraphics from '../info_graphics/MiniInfoGraphics';
import MiniTypeWriter from './MiniTypeWriter';

type Type10MiniProps = {
    slideIndex: number;
    title: string;
    description?: string;
    design_index: number;
    infographics: {
        title: string;
        description: string;
        chart: {
            chart_type: string;
            value: {
                number_type: string;
                numerical: number;
                suffix: string;
                numerator?: number;
                denominator?: number;
                percentage?: number;
            }
        }
    }[];
}

const Type10Mini = ({ slideIndex, title, description, infographics, design_index }: Type10MiniProps) => {

    if (infographics.length === 1) {
        return (
            <div className="slide-container border shadow-xl  border-gray-200 max-h-[150px] aspect-video rounded-lg pointer-events-none flex items-center justify-center p-2 w-full">
                <div className="grid grid-cols-2 gap-4 w-full">
                    <div>
                        <p className='text-[8px] slide-title font-semibold'>
                            <MiniTypeWriter text={title} />
                        </p>
                        {description && <p className='text-[6px] slide-description'>
                            <MiniTypeWriter text={description} />
                        </p>}
                    </div>
                    <div>
                        <MiniInfoGraphics slideIndex={slideIndex} itemIndex={0} chart={infographics[0].chart} />
                        <p className='text-[6px] font-medium slide-description'>
                            <MiniTypeWriter text={infographics[0].description} />
                        </p>
                    </div>
                </div>
            </div>
        )
    } else {


        return (
            <div className='w-full aspect-video border  shadow-xl border-gray-200 bg-white p-4 flex rounded-lg flex-col items-center justify-center slide-container'>
                <div className="text-center mb-4">
                    <p className='text-[8px] slide-title font-semibold'>
                        <MiniTypeWriter text={title} />
                    </p>
                    {description && <p className='text-[6px] slide-description'>
                        <MiniTypeWriter text={description} />
                    </p>}
                </div>
                <div style={{ gridTemplateColumns: `repeat(${infographics.length}, 1fr)` }} className='grid w-full gap-1'>
                    {infographics.map((item, index) => (
                        <div key={index} className={`text-center p-1  ${design_index === 1 ? 'slide-box rounded-lg ' : ''}`}>
                            <MiniInfoGraphics slideIndex={slideIndex} itemIndex={index} chart={item.chart} />
                            <p className='text-[6px] line-clamp-1 font-medium slide-heading'>
                                <MiniTypeWriter text={item.title} />
                            </p>
                            <p className='text-[5px] line-clamp-2 font-medium slide-description'>
                                <MiniTypeWriter text={item.description} />
                            </p>
                        </div>
                    ))}
                </div>
            </div>
        )
    }
}

export default Type10Mini
