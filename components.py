css = '''
    <style>
        body{
            height: 100vh;
            display: flex;
            background: #4070f4;
            align-items: center;
            justify-content: center;
        }
        .skill-box{
            width: 100%;
            margin: 34px 0;
        }
        .skill-box .title{
            display: block;
            font-size: 14px;
            font-weight: 600;
            color: #3166b1;
        }
        .skill-box .skill-bar{
            height: 8px;
            width: 100%;
            border-radius: 6px;
            margin-top: 6px;
            background: rgba(0,0,0,0.1);
        }
        .skill-bar .skill-per{
            position: relative;
            display: block;
            height: 100%;
            border-radius: 6px;
            background: #3166b1;
            animation: progress 0.4s ease-in-out forwards;
            opacity: 0;
        }
        @keyframes progress {
            0%{
                width: 0;
                opacity: 1;
            }
            100%{
                opacity: 1;
            }
        }
        .skill-per .tooltip{
            position: absolute;
            right: -24px;
            top: 16px;
            font-size: 9px;
            font-weight: 500;
            color: #fff;
            padding: 2px 6px;
            border-radius: 3px;
            background: #3166b1;
            z-index: 1;
        }
        .tooltip::before{
            content: '';
            position: absolute;
            left: 50%;
            bottom: 10px;
            height: 10px;
            width: 10px;
            z-index: -1;
            background-color: #3166b1;
            transform: translateX(-50%) rotate(45deg);
        }
    </style>
'''

progress_bars_template = """
    <div class="skill-box">
        <span class="title">Glaucoma</span>
        <div class="skill-bar">
            <span class="skill-per" style="width: {{GLAUCOMA_PROBABILITY}}%">
                <span class="tooltip">{{GLAUCOMA_PROBABILITY}}%</span>
            </span>
        </div>
    </div>
    <div class="skill-box">
        <span class="title">Cataract</span>
        <div class="skill-bar">
            <span class="skill-per" style="width: {{CATARACT_PROBABILITY}}%">
                <span class="tooltip">{{CATARACT_PROBABILITY}}%</span>
            </span>
        </div>
    </div>
    <div class="skill-box">
        <span class="title">Diabetic Retinopathy</span>
        <div class="skill-bar">
            <span class="skill-per" style="width: {{DR_PROBABILITY}}%">
                <span class="tooltip">{{DR_PROBABILITY}}%</span>
            </span>
        </div>
    </div>
    <div class="skill-box">
        <span class="title">Hypertensive Retinopathy</span>
        <div class="skill-bar">
            <span class="skill-per" style="width: {{HYPERTENSIVE_PROBABILITY}}%">
                <span class="tooltip">{{HR_PROBABILITY}}%</span>
            </span>
        </div>
    </div>
    <div class="skill-box">
        <span class="title">Branch Retinal Vein Occlusion (BRVO)</span>
        <div class="skill-bar">
            <span class="skill-per" style="width: {{BRVO_PROBABILITY}}%">
                <span class="tooltip">{{BRVO_PROBABILITY}}%</span>
            </span>
        </div>
    </div>
    <div class="skill-box">
        <span class="title">Central Retinal Vein Occlusion (CRVO)</span>
        <div class="skill-bar">
            <span class="skill-per" style="width: {{CRVO_PROBABILITY}}%">
                <span class="tooltip">{{CRVO_PROBABILITY}}%</span>
            </span>
        </div>
    </div>
    <div class="skill-box">
        <span class="title">Retinal Artery Occlusion (RAO)</span>
        <div class="skill-bar">
            <span class="skill-per" style="width: {{RAO_PROBABILITY}}%">
                <span class="tooltip">{{RAO_PROBABILITY}}%</span>
            </span>
        </div>
    </div>
"""