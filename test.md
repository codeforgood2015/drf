## Overview
The Optical character recognition(OCR) is one of the most well-researched areas of computer visions, pattern recognition and artificial intelligence.  The main goal of OCR is to convert images of typed, handwritten, or printed text into a machine-encoded text.  The type of texts (i.e. typed, handwritten, or printed) projects different chanllenges and greatly influences the mechanism through which a machine can extract textual information.  For this project, we focus on typed texts. Even though we constain the input type to typed texts, there are still many variations such as font type and size that makes our project an challenging task.  The OCR consists of multiple stages. 

    
###1. Review 1
    Title: Optical Character Recognition (OCR) - How it works. (Feb 5, 2012) 
    Author: Nicomsoft OCR SDK Knowldge base

This article from Nicomsoft OCR SDK developers explains each stage of the OCR.  The first step is to get a image of the source we want to extract the text from  We can use scanners or digital cameras to take the image and load it as machine-reading language, i.e. bits, using a bitmap.  Bitmap is a mapping from one domain (for example, a range of integers) to bits (1 or 0). The second step is to preprocess the image.  Preprocessing involves modifying the resolution, inverting the image to better detect the most important image features.  It also involves rescaling and deskewing the image to fit the predefined range of values by the subsequent algorithms.  It should also denoise the image to improve the image quality. Another important step in the preprocessing is to convert color or gray image to black-white image: "binarization", and to detect and amalze page layout: "zoning".

The second step is the main algorithm of OCR, the recognition of characters. This algorithm takes each character and returns one or more possible candidate character code.  This processes involve pattern recognition, and/or feature extraction.

The last step is post-processing that finalize the character code from the list of possible candidate codes. With the help of dictionary or inference on context of the text, the algorithm decides the most probable character code. For example, one can use "near-neightbor analysis" that make use of co-occurrence frequencies to correct errors based on the knowledge on what words tend to appear together. 

    How does it relate to my project?
Each of these steps involves many parameters that need to be well-tuned for the OCR system to work properly.  Since my project involves reading texts printed on different materials, such as A4 paper, newspaper or recycled paper (books), as well as various font sizes,  it is an interesting question how we can train the algorithms to adjust to these different environments while maintaining/improving their performances. 

###2. Review 2
    Title: "The Type-Reading Optophone-An Instrument Which Enables the Blind to Read Ordinary Print", Scientific American Monthly 109-110. October 1920.
    
This article explains the improved version of the type-reading optophone. Edmund Fournier d'Albe developed the first optophone that produced tones corresponding to the specific characters while scanning acorss a printed page. It is referred as a "white-sounding" optophone since white spaces, not black letters, produce notes. In other words, the black letters were recognized by the notes absent in the scale, rather than by the notes which remain sounding.  This article explains two modifications introduced by Messrs.Barr and Stroud.  Barr and Stroud (?) added a cylindrical rod made of selenium in order to turn the original device to produce a sound corresponding to the black letter, while remaining silent when white paper is exposed.  This new mechanism is called "black-sounding" in comparions to the original white sounding. They also added three middle lenses so that a blind reader could easily adjust the appratus to different size of type, length of line and line interval. 

    How does it relate to my project?
It explains how this old, yet innovative reading device uses optics and sounds to enable a blind person to read texts. Even though this invention dates back to 1920, it tackled similar problems the modern OCR deals with.  I learned that many aspects of preprocessing the image before the main OCR algorithm runs can be improved with the help of hardware, such as the "middle lens" added by Dr. Stroud. 

###3. Review 3
    Title: Ray Smith (2007). "An Overview of the Tesseract OCR Engine" (PDF). Retrieved 2013-05-23.
 
 The author is the original developer of an optical character recognition engine for various operation systems, called Tesseract. It is one of the most advanced OCR engines, and it is free software sponsored by Goolge since 2006. The paper discusses key features unique to Tesseract. Compared to other softwares, it provides improvements in line and word fining and word recognition accuracy, using static character classifier,linguistic analysis, and the adaptive classifier.  

     How does it relate to my project?
Based on the research on different free OCR softwares, thhe Tesseract is the most advanced and most available resource.  We will start exploring this tool to learn how it exactly works and how we can trim down its features and modify it to fit inside the light-weight and simply device we are aiming for. 
 
