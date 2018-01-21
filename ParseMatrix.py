from TextSimilar import cosine_sim

test1 = """President Trump believes the politics over illegal immigration are a distraction technique employed by Democrats.

The deadline arrived without a deal. The U.S. government shut down at midnight Friday after Congress failed to overcome a partisan divide over immigration and spending.

In a late-night vote, Senate Democrats joined to block a bill that would have kept the government running until mid-February. A flurry of last-minute negotiations failed to produce an agreement.

Democrats tried to use the Friday night funding deadline to win concessions from Republicans, including an extension of DACA, an Obama-era program protecting some young immigrants from deportation. The program is set to expire in March. Republicans sought more time for talks, but Democrats refused.

The shutdown is only the fourth government closure in a quarter-century. It will only partially curb government operations.

Uniformed service members, health inspectors, and law enforcement officers are set to work without pay. But Social Security and most other safety net programs are unaffected.

Not looking good for our great Military or Safety & Security on the very dangerous Southern Border. Dems want a Shutdown in order to help diminish the great success of the Tax Cuts, and what they are doing for our booming economy.

— Donald J. Trump (@realDonaldTrump) January 20, 2018
If no deal is brokered by Monday, hundreds of thousands of federal employees are set to be furloughed.

The White House and Capitol Hill will be working with skeleton staffs, but some government agencies, like the Environmental Protection Agency, have said they were able to shift funding around to keep most workers on the job. National parks and federal museums will be open, but with potentially reduced services.

Earlier Friday night, President Donald Trump seemed pessimistic that a deal could be reached in time.

Here’s where we’re at: 

Republicans – who control the House, Senate, and WH – are on the verge of making #TrumpShutdown a reality because they refuse to protect DREAMers and provide long-term certainty for our military, the opioid crisis, CHIP, and other key issues.

— Nancy Pelosi (@TeamPelosi) January 20, 2018
"Not looking good for our great Military or Safety & Security on the very dangerous Southern Border," the president tweeted. "Dems want a Shutdown in order to help diminish the great success of the Tax Cuts, and what they are doing for our booming economy." """
test2 = """Recriminations have begun over the failure of the US Senate to pass a new budget and prevent the shutdown of many federal services.

A bill to fund the federal government for the coming weeks did not receive the required 60 votes by the deadline of midnight on Friday.

President Trump accused the Democrats of putting politics above the interests of the American people.

The Democrats blame him for rejecting bipartisan compromise proposals.

Both the Republican and Democrat congressional leaders say they will keep talking, and the White House budget chief has expressed optimism that a resolution will be found before Monday.

But if not, hundreds of thousands of federal workers face the prospect of no work and shuttered offices at the start of the working week.

The last government shutdown was in 2013, and lasted for 16 days.

Why can the two sides not agree?

This is the first time a government shutdown has happened while one party, the Republicans, controls both Congress and the White House.

The vote on Friday was 50-49, falling far short of the 60 needed to advance the bill. With a 54 seat majority in the Senate, the Republicans did not have enough seats to pass the bill without some support from the Democrats.

They want funding for border security - including the border wall - and immigration reforms, as well as increased military spending.

The Democrats have demanded protection from deportation of more than 700,000 undocumented immigrants who entered the US as children. """
test3 = """But maybe the reason Trump’s behavior should bother us is bigger than the notion that a commander in chief should meet a rigorous standard of morality just because. Maybe it has more to do with the practical pitfalls that breaches such as this one carry with them.

There’s evidence that Daniels wasn’t the only woman to book alone time with the then-reality TV star. In “Fire and Fury,” Michael Wolff quotes former chief strategist Stephen K. Bannon as asking, “What did we have, a hundred women?” before saying that a lawyer “took care of all of them.”

Adult performer Jessica Drake accused Trump of offering her $10,000 for sex the same year he allegedly slept with Daniels, and she claims she can’t say more because of a nondisclosure agreement. And, according to a separate Journal story from just four days before the election, the company that owns the Trump-friendly National Enquirer awarded a former Playboy centerfold model $150,000 for the rights to her story of an affair with Trump in, yes, 2006 again. Then, the tabloid quashed it.

The problem here isn’t Trump’s repeated ethical lapses alone, although they do induce a certain squeamishness. The problem is the possibility of blackmail against a presidential team willing to pay big to cover up misbehavior.

Trump’s actions, clearly, are out of sync with our collective ethical code: Eighty-four percent of Americans disapprove of adultery, and probably more than that disapprove of adultery that occurs with a porn star four months after a man’s wife gives birth to their first child together. By breaking that code and then aspiring to an office that requires the support of Americans who abide by it (or at least believe they do), any politician puts himself in a vulnerable position. Either he risks a ruined career, or he does whatever he can to quiet things down.

When that politician is the president, whoever’s in the know wields a dangerous amount of power over a figure who himself is tremendously powerful. If a foreign country acquires damning information about the United States’ leader, it could, either by threatening to expose past indiscretions or by laying a sexual trap, twist international policy to its benefit. A domestic group could also hold dirty little secrets over the man in charge to draw special favors.

That — not some vague concept of the president as perfect role model — is what makes it newsworthy that a president or presidential contender may have paid a bunch of people not to say they had adulterous sex with him. Trump’s case differs a bit from the typical politician’s; he didn’t have much good-guy credit to start with, and whatever he did possess he has long since spent, so the Daniels affair doesn’t seem to have hurt him so far. But it doesn’t matter whether an admission from someone such as Daniels does hurt Trump. It only matters that he thinks it might. We’ve now heard from multiple women who claim that Trump slept with them and didn’t want the world to find out. We’ve heard that his lawyer went through contortions to hush up a hush-up. What we don’t know is what else the president and all his men would do to keep something hidden. New details about the Stormy Daniels situation emerge every day now, all unverified. They include tales about Trump’s preferences and peculiarities, from his fondness for Forbes magazine to the comparison Daniels says he made between her and his “beautiful, smart” daughter. The salaciousness entertains us, and it repulses us, too. But it’s the secrecy that should scare us.

 """

similarityMatrix = cosine_sim(test1, test2, test3)

