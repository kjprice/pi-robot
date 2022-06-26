import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import Dropdown from 'react-bootstrap/Dropdown';
import DropdownButton from 'react-bootstrap/DropdownButton';

import { setServerProcessedClassificationModel } from '../../../redux/actions/server-actions';
import { CLASSIFICATION_MODELS } from '../../../redux/constants/server-constants';
import { sendNewClassificationModel } from '../../../api/handle-socket-connections';

function formatClassificationModelName(classificationModel) {
  return classificationModel.replaceAll('_', ' ');
}

const mapStateToProps = (props) => {
  const { serverReducers } = props;
  const { classificationModel } = serverReducers;
  return {
    classificationModel
  };
}

function mapDispatchToProps(dispatch) {
  return bindActionCreators({ setServerProcessedClassificationModel }, dispatch)
}

function dropDownTitle(selectedClassificationModel) {
  return `Classification Model: ${formatClassificationModelName(selectedClassificationModel)}`;
}

function newModelClick(onSelect, modelName) {
  onSelect(modelName);
  sendNewClassificationModel(modelName);
}

function ModelDropdownOption(props) {
  const {modelName, isSelected, onSelect} = props;

  return (
    <Dropdown.Item active={isSelected} onClick={() => newModelClick(onSelect, modelName)}>
      {formatClassificationModelName(modelName)}
    </Dropdown.Item>
  )
}

function ImageRecognitionDropdown(props) {
  const { classificationModel } = props;
  const classificationModels = Object.keys(CLASSIFICATION_MODELS);
  return (
    <DropdownButton title={dropDownTitle(classificationModel)}>
      {classificationModels.map(modelName => (
        <ModelDropdownOption
          key={modelName}
          modelName={modelName}
          isSelected={modelName === classificationModel}
          onSelect={props.setServerProcessedClassificationModel}
          />
        ))}
    </DropdownButton>
  )
}

export default connect(mapStateToProps, mapDispatchToProps)(ImageRecognitionDropdown);