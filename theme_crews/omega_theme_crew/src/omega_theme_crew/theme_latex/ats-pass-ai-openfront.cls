% Intro Options
\ProvidesClass{ats-pass-ai-openfront}[2019/01/01 ATS AI Open Front Page]
\NeedsTeXFormat{LaTeX2e}
\DeclareOption{print}{\def\@cv@print{}}
\DeclareOption*{%
  \PassOptionsToClass{\CurrentOption}{article}
}
\ProcessOptions\relax
\LoadClass{article}

% Package Imports
\usepackage[hmargin=1.25cm, top=0.45cm, bottom=0.4cm]{geometry}
\usepackage[hidelinks]{hyperref}
\usepackage{soul} % underlining links
\usepackage{calc} % for simple arithmetic
\usepackage{ifthen} % for if else statements
\usepackage{afterpage}

% Publications
\usepackage{cite}
\usepackage{enumitem} % for tight lists
\renewcommand\refname{\vskip -1.5cm}

% Color definitions
\usepackage[usenames,dvipsnames]{xcolor} 
\definecolor{date}{HTML}{666666} 
\definecolor{primary}{HTML}{2b2b2b} 
\definecolor{headings}{HTML}{6A6A6A}
\definecolor{subheadings}{HTML}{333333}

% Set main fonts
\usepackage{fontspec}

\setmainfont[
  Color=primary, 
  Path = fonts/lato/,
  BoldItalicFont=Lato-RegIta,
  BoldFont=Lato-Bol,
  ItalicFont=Lato-LigIta
]{Lato-Lig} % using Lato Light as the main font

\setsansfont[
  Scale=MatchLowercase,
  Mapping=tex-text,
  Path = fonts/raleway/, % Adjusted path; use relative or absolute as necessary
  UprightFont = Raleway-ExtraLight, % Specifying the font file
  BoldFont = Raleway-SemiBold.ttf, % Correctly specifying the bold font file
  ItalicFont = Raleway-Italic.ttf, % Adding italic font for completeness
  BoldItalicFont = Raleway-BoldItalic.ttf, % Adding bold italic font
  Extension = .ttf, % Adding extension if LaTeX struggles with recognition
  Color=primary
]{Raleway}

% Define the secondary font family (Regular as default)
\newfontfamily\itemFont[
  Path = ./fonts/raleway/,
  Extension = .ttf,
  UprightFont = *-Light,
  BoldFont = *-SemiBold,
  ItalicFont = *-Italic,
  BoldItalicFont = *-BoldItalic
]{Raleway}

% Date command
\usepackage[absolute]{textpos}
\usepackage[UKenglish]{isodate}
\setlength{\TPHorizModule}{1mm}
\setlength{\TPVertModule}{1mm}

\newcommand{\lastupdated}{\begin{textblock}{60}(151,5)
\raggedleft
\color{date}\fontspec[Path = fonts/raleway/]{Raleway-ExtraLight}\fontsize{8pt}{10pt}\selectfont 
Last Updated on \\
  \today
\end{textblock}}

% Name command
\newcommand{\namesection}[3]{
  \centering{
  \fontsize{40pt}{60pt}
  \fontspec[Path = fonts/lato/]{Lato-Hai}\selectfont #1 
  \fontspec[Path = fonts/lato/]{Lato-Lig}\selectfont #2
  } \\[5pt]
  \centering{
  \color{headings}
  \fontspec[Path = fonts/raleway/]{Raleway-Medium}\fontsize{11pt}{14pt}\selectfont #3}
  \noindent\makebox[\linewidth]{\color{headings}\rule{\paperwidth}{0.4pt}}
  \vspace{-10pt}
}

\setcounter{secnumdepth}{0}  % Disable section numbering
\makeatletter
\renewcommand{\section}{\@startsection{section}{1}{\z@}%
  {0pt}% Space before the section
  {5pt}% Space after the section
  {\normalfont\fontspec[Path = fonts/lato/]{Lato-Lig}\fontsize{16pt}{24pt}\selectfont\color{headings}\raggedright\uppercase}}

\renewcommand{\subsection}{\@startsection{subsection}{2}{\z@}%
  {0pt}% Space before the subsection
  {2pt}% Space after the subsection
  {\normalfont\fontspec[Path = fonts/lato/]{Lato-Bol}\fontsize{12pt}{18pt}\selectfont\color{subheadings}\raggedright\uppercase}}
\makeatother

\newlength{\headingwidth}
\newcommand{\setHeadingWidth}[1]{\settowidth{\headingwidth}{\uppercase{#1}}} % Measure the width of the heading

\newcommand{\headingtwo}[1]{
  \setHeadingWidth{#1} % Set the width of the heading
  \vspace{5pt}
  % \color{headings}
  % Adjust font size based on the width of the heading
  \ifdim\headingwidth<7.5cm
  \color{headings}
    \fontspec[Path = fonts/lato/]{Lato-Bol}\fontsize{12pt}{14pt}\selectfont
  \else
  \color{primary}
    \fontspec[Path = fonts/lato/]{Lato-Reg}\fontsize{11pt}{13pt}\selectfont
  \fi
  \uppercase{#1} % Convert the heading to uppercase
  \par
  \normalfont
  \vspace{3pt}
}



% Volunteer section itemize
\newenvironment{vitemize}{  % Accepts one parameter
\vspace{-5pt}  % Use the parameter to add vertical space
\itemFont  % Set the font family
\fontsize{11pt}{14pt}\selectfont  % Set the font size
\begin{itemize}[leftmargin=*] \itemsep1pt \parskip0pt \parsep0pt  % Start itemize with fewer gaps
}{  
\end{itemize}
}


% career goal body
\newcommand{\careerGoalBody}[1]{
{\color{headings}\raggedright\fontspec[Path = fonts/lato/]{Lato-Lig}\fontsize{12pt}{14pt}\selectfont {#1\\}\par\vspace{3pt}}

% raleway font
% {\color{headings}\raggedright\fontspec[Path = fonts/raleway/]{Raleway-Light}\fontsize{12pt}{15pt}\selectfont {#1\\}\par}}

}

% -------------- Experience section -------

\newlength{\titleWidth}
\newcommand{\setTitleWidth}[1]{\settowidth{\titleWidth}{\uppercase{#1}}} % Count and then set the width of the title

\newlength{\summaryPointsWidth}
\newcommand{\setSummaryPointsWidth}[1]{\settowidth{\summaryPointsWidth}{#1}} 

\newlength{\myTotalWidth}

\newcommand{\customTitle}[1]{
  \setTitleWidth{#1} % Set the width of the title
  \setlength{\myTotalWidth}{\titleWidth}
  \vspace{5pt}
\color{subheadings}\fontspec[Path = fonts/lato/]{Lato-Bol}\fontsize{13pt}{12pt}\selectfont\uppercase {#1} \normalfont\vspace{3pt}}


\newcommand{\summaryPoints}[1]{
  \setSummaryPointsWidth{#1} % Set the width of the summary points
  \addtolength{\myTotalWidth}{\summaryPointsWidth} 
  \hspace{-5pt} % Adjust the horizontal space
  \color{subheadings}\raggedright\fontspec[Path = fonts/raleway/]{Raleway-Regular}\fontsize{11pt}{13pt}\selectfont
  % Check if the title width is greater than a specific length
  \typeout{-----: \the\myTotalWidth}
  \ifdim\myTotalWidth>296pt
    \par\noindent{#1\\}\vspace{4pt} % Ensure no indentation at the start of a new paragraph
  \else
  \hspace{-6pt}
    { | #1\\} % Ensure space starts before the content if not on a new line
  \fi
}

\newcommand{\roleAndTimeline}[1]{
  {\color{headings}\raggedright\fontspec[Path = fonts/raleway/]{Raleway-Regular}\fontsize{11pt}{10pt}\selectfont {#1\\}\par}}

\newcommand{\shortDescription}[1]{
  \vspace{\betweenDescriptionVSpace} % Add vertical space before the description
  {\color{headings}\raggedright\itemFont\fontsize{11pt}{13pt}\selectfont {#1\\}\par} % Corrected to use #2
}

% Bullet Lists with fewer gaps command
\newenvironment{tightemize}{  % Accepts one parameter
\vspace{\titemizeVSpaceAdjustment}  % Use the parameter to add vertical space
\itemFont  % Set the font family
\fontsize{11pt}{14pt}\selectfont  % Set the font size
\begin{itemize}\itemsep5pt \parskip0pt \parsep0pt  % Start itemize with fewer gaps
}{  
\end{itemize}
\vspace{\titemizeVSpaceAdjustment}
}

% -----------------------------------

% Descriptors command
\newcommand{\semiTitle}[1]{
\color{subheadings}\raggedright\fontspec[Path = fonts/raleway/]{Raleway-Medium}\fontsize{12pt}{13pt}\selectfont {\\#1}\par\vspace{2pt} \normalfont}

% SubTitle command
\newcommand{\subTitle}[1]{
{\color{headings}\raggedright\fontspec[Path = fonts/raleway/]{Raleway-Medium}\fontsize{12pt}{14pt}\selectfont {#1\\}\par}}


\newcommand{\body}[1]{
  % \color{subheadings}
  {\raggedright
  \fontspec[Path = fonts/lato/]{Lato-Lig}
  \fontsize{12pt}{15pt}\selectfont  % Adjusted line spacing here
  {#1\par}  % Added specific spacing after the command
  \normalfont
  \skillsVSpace
  }
}