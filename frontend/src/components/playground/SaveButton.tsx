interface Props {

    save: () => Promise<void>;

}

export default function SaveButton({

    save,

}: Props) {

    return (

        <button

            className="playground-save"

            onClick={() => {

                void save();

            }}

        >

            Save Settings

        </button>

    );

}