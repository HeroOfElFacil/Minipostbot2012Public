import matplotlib.pyplot as plt
import usosprzedmioty


def zapisz_plan(zajecia: list):
    rooms = ['Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek']

    day_labels = ['Randomplan']

    fig = plt.figure(figsize=(10, 8))
    for pwp in zajecia:
        event = pwp.name
        room = pwp.day - 0.48
        start = pwp.start + 15/60 # full hours + 15 min
        end = start + pwp.dur / 60
        # plot event
        art = plt.fill_between([room, room + 0.96], [start, start], [end, end], color='wheat', edgecolor='k',
                         linewidth=0.5)
        art.set_edgecolor('k')
        # plot beginning time
        plt.text(room + 0.02, start + 0.05, '{0}:{1:0>2}'.format(pwp.start, 15), va='top', fontsize=7)
        # plot event name
        plt.text(room + 0.48, (start + end) * 0.5, event, ha='center', va='center', fontsize=11)

        # Set Axis
        ax = fig.add_subplot(111)
        ax.yaxis.grid()
        ax.set_xlim(0.5, len(rooms) + 0.5)
        ax.set_ylim(21.1, 7.9)
        ax.set_xticks(range(1, len(rooms) + 1))
        ax.set_xticklabels(rooms)
        ax.set_ylabel('Time')

        # Set Second Axis
        ax2 = ax.twiny().twinx()
        ax2.set_xlim(ax.get_xlim())
        ax2.set_ylim(ax.get_ylim())
        ax2.set_xticks(ax.get_xticks())
        ax2.set_xticklabels(rooms)
        ax2.set_ylabel('Time')

        plt.title(day_labels[0], y=1.07)
        plt.savefig('plan.png'.format(day_labels[0]), dpi=200)
